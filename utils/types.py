from typing import Tuple
from pygame import Surface
from pygame.math import Vector2
from pygame.sprite import Group, Sprite
from pygame.colordict import THECOLORS as colors
from abc import abstractmethod
import pygame
from typing import List
from GUI.field import *


class GameElement(Sprite):
    def __init__(self, *groups, color=colors.get("white"),**kwargs) -> None:
        super().__init__()
        self._x, self._y = (0, 0)
        self._orientation = 0
        self._vel = 0
        self.size = (1,1)
        self.inertia = 1
        self.asset = ''
        for group in groups:
            if isinstance(group, Group):
                self.add(group)
        for k, v in kwargs.items():
            alt_key = '_' + k
            if self.__dict__.get(k, None) != None:
                self.__dict__.update({k: v})
            elif self.__dict__.get(alt_key, None) != None:
                self.__dict__.update({alt_key: v})
        if self.asset != '':
            self._surface = pygame.image.load(self.asset)
            self._surface = pygame.transform.scale_by(self._surface, self.size/self._surface.get_height())
        else:
            self._surface = Surface(self.size)
            self._surface.fill(color)
        self._surface.set_colorkey(colors.get("black"))

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
