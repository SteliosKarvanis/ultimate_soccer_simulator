from typing import Tuple
import pygame
from pygame import Surface, sprite
from utils.types import GameElement, colors
from GUI.field import LEFT_FRONT_GOAL_X, FIELD_LENGTH_Y, TOP_GOAL_Y
from utils.configs import SAMPLE_TIME
from GUI.player import Player
import math

class Ball(GameElement):
    def __init__(self, players_group: sprite.Group, *args, **kwargs):
        super().__init__(*args, size = (25, 25), **kwargs)
        self._surface = pygame.image.load("resources/ball.png")
        self._surface = pygame.transform.scale_by(self._surface, self.size[1]/self._surface.get_height())
        self._surface.set_colorkey(colors.get("black"))
        self.add_internal(players_group)

    def update(self) -> str:
        pass
