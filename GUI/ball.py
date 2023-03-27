from typing import Tuple
import pygame
from pygame import Surface
from utils.types import GameElement

BALL_RADIUS = 2


class Ball(pygame.sprite.Sprite, GameElement):
    def __init__(self, initial_pos: Tuple = (0, 0)):
        super().__init__()
        self._x, self._y = initial_pos
        self._vel = 0
        self._orientation = 0
        self._radius = BALL_RADIUS
        self._sprite = pygame.image.load("resources/ball.png")
        self._sprite = pygame.transform.scale(self._sprite, (30, 30))

    def update(self, action):
        pass

    def get_sprite(self) -> Surface:
        return self._sprite
