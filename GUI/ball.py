from typing import Tuple
import pygame
from pygame import Surface
from utils.types import GameElement
from GUI.field import LEFT_FRONT_GOAL_X, FIELD_LENGTH_Y, TOP_GOAL_Y
from utils.configs import SAMPLE_TIME
from GUI.player import Player
import math


BALL_RADIUS = 12
FRICTION = 4
BALL_DIAMETER = 2 * BALL_RADIUS
EPSILON = 1


def change_reference_frame(params: tuple, rf_params: tuple) -> tuple:
    rf_x, rf_y, rf_theta, rf_v = rf_params
    x0, y0, theta0, v0 = params
    e_vx = v0 * math.cos(theta0 * math.pi / 180) - rf_v * math.cos(rf_theta * math.pi / 180)
    e_vy = v0 * math.sin(theta0 * math.pi / 180) - rf_v * math.sin(rf_theta * math.pi / 180)
    e_x = x0 - rf_x
    e_y = y0 - rf_y
    v = math.sqrt(e_vx**2 + e_vy**2)
    if e_vx > 0.0 and v != 0:
        theta = (int(math.asin(e_vy / v) * 180 / math.pi) - rf_theta) % 360
    elif e_vx < 0.0 and v != 0:
        theta = (180 - int(math.asin(e_vy / v) * 180 / math.pi) - rf_theta) % 360
    else:
        if e_vy > 0.0:
            theta = (90 - rf_theta) % 360
        elif e_vy < 0.0:
            theta = (270 - rf_theta) % 360
        else:
            theta = 0
    x = e_x * math.cos(rf_theta * math.pi / 180) + e_y * math.sin(rf_theta * math.pi / 180)
    y = -e_x * math.sin(rf_theta * math.pi / 180) + e_y * math.cos(rf_theta * math.pi / 180)
    new_params = (x, y, theta, v)
    return new_params


def back_to_original_frame(params: tuple, rf_params: tuple) -> tuple:
    rf_x, rf_y, rf_theta, rf_v = rf_params
    x, y, theta, v = params
    x0 = x * math.cos(rf_theta * math.pi / 180) - y * math.sin(rf_theta * math.pi / 180) + rf_x
    y0 = x * math.sin(rf_theta * math.pi / 180) + y * math.cos(rf_theta * math.pi / 180) + rf_y
    vx0 = v * math.cos((theta + rf_theta) * math.pi / 180) + rf_v * math.cos(rf_theta * math.pi / 180)
    vy0 = v * math.sin((theta + rf_theta) * math.pi / 180) + rf_v * math.sin(rf_theta * math.pi / 180)
    v0 = math.sqrt(vx0**2 + vy0**2)
    if vx0 > 0.0:
        theta0 = (int(math.asin(vy0 / v0) * 180 / math.pi)) % 360
    elif vx0 < 0.0:
        theta0 = (180 - int(math.asin(vy0 / v0) * 180 / math.pi)) % 360
    else:
        if vy0 > 0.0:
            theta0 = 90
        elif vy0 < 0.0:
            theta0 = 270
        else:
            theta0 = rf_theta + theta
    return (x0, y0, theta0, v0)


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
            self._x = self._x + math.cos(self._orientation * math.pi / 180) * self._vel * SAMPLE_TIME
            self._y = self._y + math.sin(self._orientation * math.pi / 180) * self._vel * SAMPLE_TIME
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
        x, y, orientation, v = change_reference_frame((self._x, self._y, self._orientation, self._vel), r_params)
        l1, l2 = element.size
        if x - BALL_RADIUS <= l1 / 2 and x + BALL_RADIUS >= -l1 / 2 and y < l2 / 2 and y > -l2 / 2:
            orientation = (180 - orientation) % 360
            self._x, self._y, self._orientation, self._vel = back_to_original_frame((x, y, orientation, v), r_params)
            return True

        elif (
            y - BALL_RADIUS <= l2 / 2 + EPSILON and y + BALL_RADIUS >= -l2 / 2 - EPSILON and x < l1 / 2 and x > -l1 / 2
        ):
            orientation = (-orientation) % 360
            self._x, self._y, self._orientation, self._vel = back_to_original_frame((x, y, orientation, v), r_params)
            return True
        return False
