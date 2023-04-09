from typing import Tuple
import pygame
from pygame import Surface, sprite
from utils.types import GameElement
from GUI.player import Player
from GUI.field import field, goals
from utils.configs import SAMPLE_TIME
import math
from utils.collision_handler import CollisionType


class Ball(GameElement):
    def __init__(self, players_group: sprite.Group, *groups, **kwargs):
        super().__init__(*groups, size=(25, 25), asset_path="resources/ball.png", **kwargs)
        self.add_internal(players_group)

    def update(self) -> str:
        pose_updates = (
            self._orientation,
            self._x + self._vel * math.cos(self._orientation * math.pi / 180),
            self._y + self._vel * math.sin(self._orientation * math.pi / 180),
        )
        collision_state = self.__get_update__(pose_updates)
        match collision_state:
            case CollisionType.NONE:
                self._orientation, self._x, self._y = pose_updates

            case CollisionType.BALL_PLAYER:
                player = self.group_collide(self, self.groups()[-1])[0]
                assert isinstance(player, Player)
                # self._vel =

    def __get_update__(self, updates: Tuple[float, float, float]) -> CollisionType:
        rotation, next_x, next_y = updates
        new_sprite = pygame.transform.rotate(self.image, rotation)
        rect = new_sprite.get_rect()
        rect.center = next_x, next_y
        if goals.get("left").colliderect(rect):
            return CollisionType.ON_LEFT_GOAL
        elif goals.get("right").colliderect(rect):
            return CollisionType.ON_RIGHT_GOAL
        elif not field.contains(rect):
            return CollisionType.WITH_SCENERY
        return self.check_collision()
