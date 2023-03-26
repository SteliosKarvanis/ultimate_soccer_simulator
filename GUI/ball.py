import pygame
from pygame import Surface
from utils.types import GameElement

class Ball(pygame.sprite.Sprite, GameElement):
    def __init__(self):
        super().__init__()
        self._x, self._y = (0,0)
        self._vel = 0
        self._orientation = 0
        self._radius = 2
        self._sprite = pygame.image.load("resources/ball.png")
        self._sprite = pygame.transform.scale(self._sprite, (30, 30))

    def update(self, action):
        pass

    def get_sprite(self) -> Surface:
        return self._sprite
