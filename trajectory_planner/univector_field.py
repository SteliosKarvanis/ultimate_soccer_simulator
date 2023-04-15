from typing import Dict, Tuple
from game_elements.player import Player
from pygame.math import Vector2
from math import pi, sqrt
from world_state import WorldState
import math


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
        params.dmin = 0.3
        params.delta = 0.1
        return params


class UnivectorField:
    def __init__(self, params=UnivectorFieldParams.get_default_params()):
        self.params = params

    def compute_hyperbolic_spiral_field(self, current_position: Tuple, clockwise: bool):
        teta = math.atan2(current_position[1], current_position[0])
        p = math.sqrt(current_position[0] ** 2 + current_position[1] ** 2)
        if p > self.params.de:
            if clockwise:
                return teta - (math.pi / 2) * (2 - (self.params.de + self.params.kr) / (p + self.params.kr))
            else:
                return teta + (math.pi / 2) * (2 - (self.params.de + self.params.kr) / (p + self.params.kr))
        else:
            if clockwise:
                return teta - math.pi / 2 * math.sqrt(p / self.params.de)
            else:
                return teta + math.pi / 2 * math.sqrt(p / self.params.de)

    def compute_repulsive_field(self, current_position):
        return math.atan2(current_position[1], current_position[0])

    def compute_move_to_goal_field(self, goal, current_position):
        from_goal = [current_position[0] - goal[0], current_position[1] - goal[1]]
        from_goal_rotated = [
            from_goal[0] * math.cos(-goal[2]) - from_goal[1] * math.sin(-goal[2]),
            from_goal[0] * math.sin(-goal[2]) + from_goal[1] * math.cos(-goal[2]),
        ]
        ccw = self.compute_hyperbolic_spiral_field([from_goal_rotated[0], from_goal_rotated[1] - self.params.de], False)
        cw = self.compute_hyperbolic_spiral_field([from_goal_rotated[0], from_goal_rotated[1] + self.params.de], True)
        angle = 0
        if from_goal_rotated[1] < -self.params.de:
            angle = self.normalize_angle(goal[2] + cw)
        elif self.params.de <= from_goal_rotated[1]:
            angle = self.normalize_angle(goal[2] + ccw)
        else:
            accw = [math.cos(ccw), math.sin(ccw)]
            acw = [math.cos(cw), math.sin(cw)]
            numerator = [
                accw[0] * (from_goal_rotated[1] + self.params.de) + acw[0] * (self.params.de - from_goal_rotated[1]),
                accw[1] * (from_goal_rotated[1] + self.params.de) + acw[1] * (self.params.de - from_goal_rotated[1]),
            ]
            denominator = 2 * self.params.de
            angle = self.normalize_angle(goal[2] + math.atan2(numerator[1], numerator[0]))
        # self.avoid_walls(current_position, angle)
        return angle

    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

    def avoid_walls(self, currentPosition: Tuple[float, float], angle: float, maxDistToAvoid: float) -> float:
        FIELD_LENGTH_Y = 100  # assuming FIELD_LENGTH_Y is 10
        distToHWall = FIELD_LENGTH_Y / 2 - abs(currentPosition[1])
        if distToHWall < maxDistToAvoid and angle * currentPosition[1] > 0:
            if abs(angle) < math.pi / 2:
                angle *= distToHWall / maxDistToAvoid
        return angle
