from typing import Tuple
from game_elements.field import TOP_FIELD_Y
from math import exp, pi, radians, sin, cos, sqrt, atan2
from utils.utils import cartesian_to_polar_vector, get_magnitude_from_vector, polar_to_cartesian_vector

MAX_DIST_TO_AVOID_WALL = TOP_FIELD_Y / 2


class UnivectorFieldParams:
    def __init__(self):
        self.kr = 0.1
        self.de = 0.3
        self.ko = 0.1
        self.dmin = 0.3
        self.delta = 0.1

    @classmethod
    def get_default_params(cls):
        params = cls()
        params.kr = 0.1
        params.de = 0.3
        params.ko = 0.1
        params.dmin = 0.1
        params.delta = 0.1
        return params


class UnivectorField:
    def __init__(self, params=UnivectorFieldParams.get_default_params()):
        self.params = params

    def compute_hyperbolic_spiral_field(self, current_position: Tuple[float, float], clockwise: bool):
        p, theta = cartesian_to_polar_vector(current_position[0], current_position[1])
        theta = self.normalize_angle(theta)
        if p > self.params.de:
            if clockwise:
                return theta - (pi / 2) * (2 - (self.params.de + self.params.kr) / (p + self.params.kr))
            else:
                return theta + (pi / 2) * (2 - (self.params.de + self.params.kr) / (p + self.params.kr))
        else:
            if clockwise:
                return theta - pi / 2 * sqrt(p / self.params.de)
            else:
                return theta + pi / 2 * sqrt(p / self.params.de)

    def compute_repulsive_field(self, current_position):
        _, angle = cartesian_to_polar_vector(current_position[0], current_position[1])
        angle = self.normalize_angle(angle)
        return angle

    def compute_move_to_goal_field(self, goal: Tuple[float, float, float], current_position: Tuple[float, float]):
        angle = self.normalize_angle(radians(goal[2]))
        goal = goal[0], goal[1], angle

        from_goal = [current_position[0] - goal[0], current_position[1] - goal[1]]
        from_goal_rotated = [
            from_goal[0] * cos(-goal[2]) - from_goal[1] * sin(-goal[2]),
            from_goal[0] * sin(-goal[2]) + from_goal[1] * cos(-goal[2]),
        ]
        ccw = self.compute_hyperbolic_spiral_field([from_goal_rotated[0], from_goal_rotated[1] - self.params.de], False)
        cw = self.compute_hyperbolic_spiral_field([from_goal_rotated[0], from_goal_rotated[1] + self.params.de], True)
        angle = 0
        if from_goal_rotated[1] < -self.params.de:
            angle = self.normalize_angle(goal[2] + cw)
        elif self.params.de <= from_goal_rotated[1]:
            angle = self.normalize_angle(goal[2] + ccw)
        else:
            accw = [cos(ccw), sin(ccw)]
            acw = [cos(cw), sin(cw)]
            numerator = [
                accw[0] * (from_goal_rotated[1] + self.params.de) + acw[0] * (self.params.de - from_goal_rotated[1]),
                accw[1] * (from_goal_rotated[1] + self.params.de) + acw[1] * (self.params.de - from_goal_rotated[1]),
            ]
            angle = self.normalize_angle(goal[2] + atan2(numerator[1], numerator[0]))
        return angle

    def normalize_angle(self, angle):
        while angle > pi:
            angle -= 2 * pi
        while angle < -pi:
            angle += 2 * pi
        return angle

    def avoid_walls(self, currentPosition: Tuple[float, float], angle: float) -> float:
        distToHWall = TOP_FIELD_Y - abs(currentPosition[1])
        factor = distToHWall / MAX_DIST_TO_AVOID_WALL
        if distToHWall < MAX_DIST_TO_AVOID_WALL:
            if abs(angle) <= pi / 2:
                angle *= factor
            elif currentPosition[1] > 0 and angle > 0:
                angle = pi - factor * (pi - angle)
            elif currentPosition[1] < 0 and angle < 0:
                angle *= -1
                angle = pi - factor * (pi - angle)
                angle *= -1
        return angle

    def compute_avoid_obstacle_field(
        self, current_position: Tuple[float, float], current_vel: Tuple[float, float], obstacle: Tuple[float, float]
    ):
        vs = -current_vel[0] * self.params.ko, -current_vel[1] * self.params.ko
        vs_abs = get_magnitude_from_vector(vs[0], vs[1])
        dist = get_magnitude_from_vector(obstacle[0] - current_position[0], obstacle[1] - current_position[1])
        vel = get_magnitude_from_vector(current_vel[0], current_vel[1])
        if dist >= vel * self.params.ko:
            return self.compute_repulsive_field(
                (current_position[0] - obstacle[0] - vs[0], current_position[1] - obstacle[1] - vs[1])
            )
        return self.compute_repulsive_field(
            (
                current_position[0] - obstacle[0] - vs[0] * dist / vs_abs,
                current_position[1] - obstacle[1] - vs[1] * dist / vs_abs,
            )
        )

    def compute_composed_field(
        self,
        goal: Tuple[float, float, float],
        current_position: Tuple[float, float],
        current_vel: Tuple[float, float],
        obstacle: Tuple[float, float],
    ):
        obstaclecom = self.compute_modified_obstacle(current_position, current_vel, obstacle)
        vector = current_position[0] - obstaclecom[0], current_position[1] - obstaclecom[1]
        R = get_magnitude_from_vector(vector[0], vector[1])
        # AUF = self.compute_avoid_obstacle_field(current_position, current_vel, obstaclecom)
        # if R <= self.params.dmin:
        #    return AUF
        G = exp(-pow((R - self.params.dmin) / self.params.delta, 2) / 2)
        TUF = self.compute_move_to_goal_field(goal, current_position)
        # _, angle = cartesian_to_polar_vector((1-G)*cos(TUF) + G*cos(AUF), (1-G)*sin(TUF) + G*cos(AUF))
        _, angle = cartesian_to_polar_vector((1 - G) * cos(TUF), (1 - G) * sin(TUF))
        angle = self.normalize_angle(angle)
        angle = self.avoid_walls(current_position, angle)
        return angle

    def compute_field(self, goal, current_position, current_vel, obstacle):
        obstaclecom = self.compute_modified_obstacle(current_position, current_vel, obstacle)
        vector = current_position[0] - obstaclecom[0], current_position[1] - obstaclecom[1]
        R = get_magnitude_from_vector(vector)
        AUF = self.compute_avoid_obstacle_field(current_position, current_vel, obstaclecom)
        if R <= self.params.dmin:
            return AUF
        G = exp(-pow((R - self.params.dmin) / self.params.delta, 2) / 2)
        TUF = self.compute_move_to_goal_field(goal, current_position)
        vector = polar_to_cartesian_vector(G, AUF)
        vector2 = polar_to_cartesian_vector(1 - G, TUF)
        _, angle = cartesian_to_polar_vector(vector[0] + vector2[0], vector[1] + vector2[1])
        angle = self.normalize_angle(angle)
        return angle

    def compute_modified_obstacle(self, current_position, current_vel, obstacle):
        vs = -self.params.ko * current_vel[0], -self.params.ko * current_vel[1]
        vs_abs = get_magnitude_from_vector(vs[0], vs[1])
        vector = obstacle[0] - current_position[0], obstacle[1] - current_position[1]
        dist = get_magnitude_from_vector(vector[0], vector[1])
        if dist > vs_abs:
            res = obstacle[0] + vs[0], obstacle[1] + vs[1]
        else:
            if vs_abs:
                res = obstacle[0] + vs[0] * dist / vs_abs, obstacle[1] + vs[1] * dist / vs_abs
            else:
                res = obstacle
        return res
