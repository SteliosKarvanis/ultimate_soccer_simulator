from typing import Tuple
import pygame
from pygame import Surface
from utils.types import GameElement
from GUI import field
from utils.configs import SAMPLE_TIME
import math
from utils.utils import get_screen_size

UPPER_LIMIT=31
LOWER_LIMIT=-24
LEFT_LIMIT=-42
RIGHT_LIMIT=42

BALL_RADIUS=2
FRICTION=0

class Ball(pygame.sprite.Sprite, GameElement):
    def __init__(self, initial_pos: Tuple = (0, 0)):
        super().__init__()
        self._x, self._y = initial_pos
        self._vel = 0
        self._orientation = 0
        self._radius = BALL_RADIUS
        self._sprite = pygame.image.load("resources/ball.png")
        self._sprite = pygame.transform.scale(self._sprite, (30, 30))
        self._in_camp=True
    
    def update(self):
        collision_side=self.get_bumper_state()
        if collision_side=="up" or collision_side=="down":
            self._orientation = (360-self._orientation) % 360
        elif collision_side=="right" or collision_side=="left":
            self._orientation=(180-self._orientation+360) % 360
        self._x=self._x + math.cos(self._orientation * math.pi / 180)*self._vel*SAMPLE_TIME
        self._y=self._y + math.sin(self._orientation * math.pi / 180)*self._vel*SAMPLE_TIME
        if self._vel>0:
            self._vel=self._vel-FRICTION*SAMPLE_TIME
        else:
            self._vel=0

    def get_sprite(self) -> Surface:
        return self._sprite
    #TODO: add method to check if the ball has collided with another object
    def _next_velocity(self):
        if self._vel>0:
            return self._vel-FRICTION*SAMPLE_TIME
        else:
            return 0
        
    def get_bumper_state(self):
        if self._y+BALL_RADIUS>=UPPER_LIMIT:
            return "up"
        elif self._y-BALL_RADIUS<=LOWER_LIMIT:
            return "down"
        elif self._x-BALL_RADIUS<=LEFT_LIMIT:
            return "left"
        elif self._x+BALL_RADIUS>=RIGHT_LIMIT:
            return "right"
        else:
            return "None"
        


