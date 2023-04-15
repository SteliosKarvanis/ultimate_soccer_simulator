from typing import Tuple
from pygame import Surface
from pygame.math import Vector2
from abc import abstractmethod
import pygame
from typing import List
from game_elements.field import *


class AbstractElement:
    def __init__(self) -> None:
        self._x = 0
        self._y = 0
        self._orientation = 0
        self.side = 0
        self._surface = Surface((self.side, self.side))

    def get_pos(self) -> Vector2:
        return self._x, self._y

    def get_orientation(self) -> float:
        return self._orientation

    def get_pose(self) -> Tuple[float, float, float]:
        return self._orientation, self._x, self._y

    def __is_valid_update__(self, updates: Tuple[float, float, float]) -> bool:
        rotation, next_x, next_y = updates
        new_sprite = pygame.transform.rotate(self._surface, rotation)
        rect = new_sprite.get_rect()
        rect.center = next_x, next_y
        if (
            rect.top < -TOP_FIELD_Y
            or rect.left < LEFT_FRONT_GOAL_X
            or rect.right > -LEFT_FRONT_GOAL_X
            or rect.bottom > TOP_FIELD_Y
        ):
            return False
        return True

    def get_surface(self) -> Surface:
        return self._surface
