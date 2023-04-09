from typing import Tuple, List
from pygame import Surface
from pygame.math import Vector2
from pygame.sprite import Group, Sprite
from pygame.colordict import THECOLORS as colors
import pygame
from GUI.field import *
from utils.collision_handler import CollisionType


class GameElement(Sprite):
    def __init__(self, *groups, color=colors.get("white"), **kwargs) -> None:
        super().__init__()
        self._x, self._y = (0, 0)
        self._orientation = 0
        self._vel = 0
        self.size = (1, 1)
        self.inertia = 1
        self.asset_path = ""
        for group in groups:
            if isinstance(group, Group):
                self.add(group)
        for k, v in kwargs.items():
            alt_key = "_" + k
            if self.__dict__.get(k, None) != None:
                self.__dict__.update({k: v})
            elif self.__dict__.get(alt_key, None) != None:
                self.__dict__.update({alt_key: v})
        self.image = Surface(self.size)
        if self.asset_path != "":
            img = pygame.image.load(self.asset_path)
            img = pygame.transform.scale_by(img, self.size[1] / img.get_height())
            self.image.blit(img, (0, 0))
        else:
            self.image.fill(color)
        self.image.set_colorkey(colors.get("black"))
        self._sprite = pygame.transform.rotate(self.image, self._orientation)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self._sprite.get_rect()
        self.rect.center = (self._x, self._y)

    def get_pos(self) -> Vector2:
        return self._x, self._y

    def get_orientation(self) -> float:
        return self._orientation

    def get_pose(self) -> Tuple[float, float, float]:
        return self._orientation, self._x, self._y

    def __get_update__(self, updates: Tuple[float, float, float]) -> CollisionType:
        rotation, next_x, next_y = updates
        new_sprite = pygame.transform.rotate(self.image, rotation)
        rect = new_sprite.get_rect()
        rect.center = next_x, next_y
        if not field.contains(rect):
            return CollisionType.WITH_SCENERY
        return self.check_collision()

    def check_collision(self) -> CollisionType:
        for group in self.groups():
            for element in GameElement.group_collide(self, group):
                assert isinstance(element, GameElement)
                return CollisionType.OF_PLAYERS if isinstance(element, self.__class__) else CollisionType.BALL_PLAYER
        return CollisionType.NONE

    @staticmethod
    def group_collide(sprite: Sprite, group: Group) -> List[Sprite]:
        return [element for element in pygame.sprite.spritecollide(sprite, group, False, collided=GameElement.collision_handler)]

    @staticmethod
    def collision_handler(sprite1: Sprite, sprite2: Sprite):
        collision_point = pygame.sprite.collide_mask(sprite1, sprite2)
        return collision_point != None and sprite1 != sprite2

    def get_sprite(self) -> Surface:
        return self._sprite
