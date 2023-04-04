from typing import Tuple
import pygame
from pygame import Surface
from utils.types import GameElement
from GUI.field import LEFT_FRONT_GOAL_X, FIELD_LENGTH_Y, TOP_GOAL_Y
from utils.configs import SAMPLE_TIME
import math


BALL_RADIUS = 10
FRICTION = 0
BALL_DIAMETER = 2 * BALL_RADIUS


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
        goal_state=self.get_goal_state()
        if goal_state!="None":
            self._x=0
            self._y=0
            self._vel=0
            self._orientation=0
        return goal_state

    def get_surface(self) -> Surface:
        return self._surface

    def _next_velocity(self) -> float:
        if self._vel > 0:
            return self._vel - FRICTION * SAMPLE_TIME
        else:
            return 0.0

    def get_bumper_state(self) -> str:
        if self._y + BALL_RADIUS >= FIELD_LENGTH_Y / 2:
            return "up"
        elif self._y - BALL_RADIUS <= -FIELD_LENGTH_Y / 2:
            return "down"
        elif self._y +BALL_RADIUS>=TOP_GOAL_Y or self._y-BALL_RADIUS<=-TOP_GOAL_Y:
            if self._x - BALL_RADIUS <= LEFT_FRONT_GOAL_X:
                return "left"
            elif self._x + BALL_RADIUS >= -LEFT_FRONT_GOAL_X :
                return "right"
            else:
                return  "None"
        else:
            return "None"
    
    def get_goal_state(self) -> str:
        if self._x >=-LEFT_FRONT_GOAL_X:
        #player made a goal
            return "ally"
        elif self._x <=LEFT_FRONT_GOAL_X:
        #adversary made a goal
            return "opponent"
        else:
            return "None"
