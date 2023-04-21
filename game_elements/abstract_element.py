from typing import Tuple
from math import radians
import pygame
from game_elements.field import FIELD_LENGTH_X, TOP_FIELD_Y, LEFT_FRONT_GOAL_X, TOP_GOAL_Y
from utils.utils import rotate_vector


class AbstractElement(
    pygame.sprite.Sprite,
):
    def __init__(
        self,
        initial_pos: Tuple[float, float] = (0, 0),
        orientation: float = 0,
        vel: float = 0,
        size: Tuple[float, float] = (0, 0),
    ) -> None:
        super().__init__()
        self._x, self._y = initial_pos
        self._vel = vel
        self._orientation = orientation
        self.size = size
        self._surface = pygame.Surface((1, 1))
        # Save a copy of initial state
        self.__initial_pos = initial_pos
        self.__initial_vel = vel
        self.__initial_orientation = orientation

    def get_pos(self) -> Tuple[float, float]:
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
        # Clamp angle between [0, 90[
        while rotation >= 90:
            rotation -= 90
        # Get coordinates of a vertex relative to element
        side_x, side_y = self.size
        side_x, side_y = side_x / 2, side_y / 2
        # Rotate the vertex to real position
        _, top_y = rotate_vector((side_x, side_y), -radians(rotation))
        top_x, _ = rotate_vector((side_x, side_y), -(radians(rotation - 90)))
        if next_x - top_x < -FIELD_LENGTH_X / 2 or next_x + top_x > FIELD_LENGTH_X / 2:
            return False
        if next_x - top_x < LEFT_FRONT_GOAL_X and next_y + top_y > TOP_GOAL_Y:
            return False
        if next_x - top_x < LEFT_FRONT_GOAL_X and next_y - top_y < -TOP_GOAL_Y:
            return False
        if next_x + top_x > -LEFT_FRONT_GOAL_X and next_y + top_y > TOP_GOAL_Y:
            return False
        if next_x + top_x > -LEFT_FRONT_GOAL_X and next_y - top_y < -TOP_GOAL_Y:
            return False
        if next_y + top_y > TOP_FIELD_Y or next_y - top_y < -TOP_FIELD_Y:
            return False
        return True

    def get_surface(self) -> pygame.Surface:
        return self._surface

    def reset_state(self):
        self._vel = self.__initial_vel
        self._orientation = self.__initial_orientation
        self._x, self._y = self.__initial_pos
