from typing import Tuple
import pygame
from pygame import Surface, sprite
from utils.types import GameElement, colors
from GUI.field import LEFT_FRONT_GOAL_X, FIELD_LENGTH_Y, TOP_GOAL_Y
from utils.configs import SAMPLE_TIME
import math
from utils.collision_handler import CollisionType

class Ball(GameElement):
    def __init__(self, players_group: sprite.Group, *groups, **kwargs):
        super().__init__(*groups, size=(25, 25), asset_path="resources/ball.png", **kwargs)
        self.add_internal(players_group)

    def update(self):
        pos_updates = (
            self._x + self._vel * math.cos(self._orientation * math.pi / 180),
            self._y + self._vel * math.sin(self._orientation * math.pi / 180),
        )
    def __get_update__(self, updates: Tuple[float, float, float]) -> CollisionType:
        return super().__get_update__(updates)
        

