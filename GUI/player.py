import pygame
from pygame import Surface
from utils.types import GameElement
from typing import Tuple, Optional
from constants import *
import math

class Player(pygame.sprite.Sprite, GameElement):
    def __init__(
        self, initial_pos: Tuple = (0, 0), orientation: float = 0, color=colors.get("white"), scale=1
    ):
        super().__init__()
        self.size = (5, 5)
        self._surface = Surface((self.size[0] * scale, self.size[1] * scale))
        self._surface.set_colorkey(BACKGROUND_COLOR)
        self._surface.fill(color)
        self.speed = 0.3
        self.ang_speed = 0.3
        self.spin_speed = 2
        self._x, self._y = initial_pos
        self._orientation = orientation

    def get_sprite(self) -> Surface:
        return self._surface
    
    def update(self, action):
        pose_updates = self.__next_pose(action)
        
        updated_values = []
        for i, update in enumerate(pose_updates):
            if not isinstance(update, float):
                updated_values.append(self.get_pose()[i])
            else:
                updated_values.append(update)

        self._orientation, self._x, self._y = tuple(updated_values)


    def __next_pose(self, action) -> Tuple[Optional[float]]:
        rotate, forward, spin = action
        if spin:
            return ((self._orientation - self.spin_speed) % 360, None, None)
        else:
            return (
                (self._orientation - rotate * self.ang_speed) % 360,
                self._x + math.cos(self._orientation * math.pi / 180) * self.speed * forward,
                self._y + math.sin(self._orientation * math.pi / 180) * self.speed * forward
                )

