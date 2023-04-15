from typing import Tuple
from pygame import Surface
from pygame.math import Vector2
from abc import abstractmethod
import pygame
from typing import List
from game_elements.field import *


class AbstractElement(
    pygame.sprite.Sprite,
):
    def __init__(
        self,
        initial_pos: Tuple[float, float],
        orientation: float = 0,
        vel: float = 0,
        size: Tuple[float, float] = (0, 0),
    ) -> None:
        super().__init__()
        self._x, self._y = initial_pos
        self._vel = vel
        self._orientation = orientation
        self.size = size
        self._surface = Surface(size)
        # Save a copy of initial state
        self.__initial_pos = initial_pos
        self.__initial_vel = vel
        self.__initial_orientation = orientation

    def get_pos(self) -> Vector2:
        return self._x, self._y

    def get_orientation(self) -> float:
        return self._orientation

    def get_pose(self) -> Tuple[float, float, float]:
        return self._x, self._y, self._orientation

    def get_vel(self) -> float:
        return self._vel

    def get_state(self) -> Tuple:
        return self._x, self._y, self._orientation, self._vel

    def __is_valid_update__(self, updates: Tuple[float, float, float, float]) -> bool:
        next_x, next_y, rotation, vel = updates
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

    def reset_state(self):
        self._vel = self.__initial_vel
        self._orientation = self.__initial_orientation
        self._x, self._y = self.__initial_pos
