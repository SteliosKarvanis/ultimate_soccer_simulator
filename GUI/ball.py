from typing import Tuple
import pygame
from utils.types import GameElement
from GUI.field import LEFT_FRONT_GOAL_X, FIELD_LENGTH_Y, TOP_GOAL_Y
from utils.configs import SAMPLE_TIME
from GUI.player import Player
from math import radians, cos, sin, degrees, sqrt, acos, pi, tan

BALL_RADIUS = 12
FRICTION = 4
BALL_DIAMETER = 2 * BALL_RADIUS
TOLERANCE = 10


def rotate_pos(x0: float, y0: float, angle_rad: float) -> Tuple[float, float]:
    x = x0 * cos(angle_rad) + y0 * sin(angle_rad)
    y = -x0 * sin(angle_rad) + y0 * cos(angle_rad)
    return x, y


def cartesian_to_polar_vector(v_x: float, v_y: float) -> Tuple[float, float]:
    v = sqrt(v_x**2 + v_y**2)
    if v != 0:
        theta_rad = acos(v_x / v)
        if v_y < 0:
            theta_rad = 2 * pi - theta_rad
    else:
        theta_rad = 0
    return v, theta_rad


def polar_to_cartesian_vector(v: float, angle_rad: float) -> Tuple[float, float]:
    return v * cos(angle_rad), v * sin(angle_rad)


def translate_pos(x0: float, y0: float, delta_x: float, delta_y: float) -> Tuple[float, float]:
    return x0 + delta_x, y0 + delta_y


def global_to_element_referential(params: Tuple, rf_params: Tuple) -> Tuple[float, float]:
    # Referential pose in world
    rf_x, rf_y, rf_theta_deg, rf_v = rf_params
    rf_theta_rad = radians(rf_theta_deg)
    v_rf_x, v_rf_y = polar_to_cartesian_vector(rf_v, rf_theta_rad)

    # Pose on global referential
    x0, y0, theta0_deg, v0 = params
    theta0_rad = radians(theta0_deg)
    v0_x, v0_y = polar_to_cartesian_vector(v0, theta0_rad)

    # Make relative positions (translation and rotation)
    x0, y0 = translate_pos(x0, y0, -rf_x, -rf_y)
    x, y = rotate_pos(x0, y0, rf_theta_rad)

    # Make relative velocities (translation and rotation)
    v0_x, v0_y = translate_pos(v0_x, v0_y, -v_rf_x, -v_rf_y)
    v_x, v_y = rotate_pos(v0_x, v0_y, rf_theta_rad)

    v, theta_rad = cartesian_to_polar_vector(v_x, v_y)
    theta_deg = degrees(theta_rad)
    new_params = (x, y, theta_deg, v)
    return new_params


def element_ref_to_global_ref(params: tuple, rf_params: tuple) -> tuple:
    # Referential pose in world
    rf_x, rf_y, rf_theta_deg, rf_v = rf_params
    rf_theta_rad = radians(rf_theta_deg)
    rf_v_x, rf_v_y = polar_to_cartesian_vector(rf_v, rf_theta_rad)

    # Pose on global referential
    x0, y0, theta0_deg, v0 = params
    theta0_rad = radians(theta0_deg)
    v0_x, v0_y = polar_to_cartesian_vector(v0, theta0_rad)

    # Make relative positions (translation and rotation)
    x, y = rotate_pos(x0, y0, -rf_theta_rad)
    x, y = translate_pos(x, y, rf_x, rf_y)

    # Make relative velocities (translation and rotation)
    v_x, v_y = rotate_pos(v0_x, v0_y, -rf_theta_rad)
    v_x, v_y = translate_pos(v_x, v_y, rf_v_x, rf_v_y)

    v, theta_rad = cartesian_to_polar_vector(v_x, v_y)
    theta_deg = degrees(theta_rad)
    new_params = (x, y, theta_deg, v)
    return new_params


class Ball(pygame.sprite.Sprite, GameElement):
    def __init__(self, initial_pos: Tuple = (0, 0)):
        super().__init__()
        self._x, self._y = initial_pos
        self._vel = 0
        self._orientation = 0
        self._radius = BALL_RADIUS
        self._surface = pygame.image.load("resources/ball.png")
        self._surface = pygame.transform.scale(self._surface, (BALL_DIAMETER, BALL_DIAMETER))

    def update(self) -> str:
        if self._vel > 0:
            collision_side = self.get_bumper_state()
            if collision_side == "up" or collision_side == "down":
                self._orientation = (360 - self._orientation) % 360
            elif collision_side == "right" or collision_side == "left":
                self._orientation = (180 - self._orientation + 360) % 360
            self._x = self._x + cos(radians(self._orientation)) * self._vel * SAMPLE_TIME
            self._y = self._y + sin(radians(self._orientation)) * self._vel * SAMPLE_TIME
            self._vel = self._vel - FRICTION * SAMPLE_TIME
        else:
            self._vel = 0.0
        goal_state = self.get_goal_state()
        if goal_state != "None":
            self._x = 0
            self._y = 0
            self._vel = 0
            self._orientation = 0
        return goal_state

    def __next_velocity(self) -> float:
        if self._vel > 0:
            return self._vel - FRICTION * SAMPLE_TIME
        else:
            return 0.0

    def get_bumper_state(self) -> str:
        if self._y + BALL_RADIUS >= FIELD_LENGTH_Y / 2:
            return "up"
        elif self._y - BALL_RADIUS <= -FIELD_LENGTH_Y / 2:
            return "down"
        elif self._y + BALL_RADIUS >= TOP_GOAL_Y or self._y - BALL_RADIUS <= -TOP_GOAL_Y:
            if self._x - BALL_RADIUS <= LEFT_FRONT_GOAL_X:
                return "left"
            elif self._x + BALL_RADIUS >= -LEFT_FRONT_GOAL_X:
                return "right"
            else:
                return "None"
        else:
            return "None"

    def get_goal_state(self) -> str:
        if self._x >= -LEFT_FRONT_GOAL_X:
            # player made a goal
            return "ally"
        elif self._x <= LEFT_FRONT_GOAL_X:
            # adversary made a goal
            return "opponent"
        else:
            return "None"

    def collision_management(self, element: Player) -> bool:
        r_params = (element._x, element._y, int(element.velocity_orientation), element.vel)
        l1, l2 = element.size
        collided = False
        # Changing to the referential of the element
        x, y, orientation, v = global_to_element_referential((self._x, self._y, self._orientation, self._vel), r_params)
        v_x, v_y = polar_to_cartesian_vector(v, orientation)
        # Check if has collision
        if abs(x) < BALL_RADIUS + l2 / 2 and abs(y) < BALL_RADIUS + l2 / 2:
            collided = True
            # Check which side collided
            y_top = l1 / 2 + BALL_RADIUS
            y_bottom = -y_top
            x_right = l2 / 2 + BALL_RADIUS
            x_left = -x_right
            # For each vertex, check it is above the line of movement of the ball, for example tr == True, check if the top right vertex is above the movement line of the ball
            tr = (y_top - y + tan(orientation) * (x_right - x)) > 0
            br = (y_bottom - y + tan(orientation) * (x_right - x)) > 0
            tl = (y_top - y + tan(orientation) * (x_left - x)) > 0
            bl = (y_bottom - y + tan(orientation) * (x_left - x)) > 0
            # right side colision
            if tr and not br and (orientation > 90 and orientation < 270):
                x = BALL_RADIUS + l2 / 2 + TOLERANCE
                v, orientation = cartesian_to_polar_vector(-abs(v_x), v_y)
            # left side colision
            elif tl and not bl and (orientation < 90 or orientation > 270):
                x = -BALL_RADIUS - l2 / 2 - TOLERANCE
                v, orientation = cartesian_to_polar_vector(-abs(v_x), v_y)
            # top side colision
            if tr and not tl and orientation > 180:
                y = BALL_RADIUS + l1 / 2 + TOLERANCE
                v, orientation = cartesian_to_polar_vector(v_x, -abs(v_y))
            # bottom side colision
            elif bl and not br and orientation < 180:
                y = -BALL_RADIUS - l2 / 2 - TOLERANCE
                v, orientation = cartesian_to_polar_vector(v_x, -abs(v_y))
        # Back to the global referential
        if collided:
            self._x, self._y, self._orientation, self._vel = element_ref_to_global_ref((x, y, orientation, v), r_params)
        return collided
