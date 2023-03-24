import pygame
from pygame import Surface
from typing import Tuple, Optional, Dict
from constants import *
import math

class Player(pygame.sprite.Sprite):
    def __init__(
        self, initial_pos: Tuple = (0, 0), orientation: float = 0, color=WHITE, scale=1
    ):
        super().__init__()
        self.size = (5, 5)
        self._surface = Surface((self.size[0] * scale, self.size[1] * scale))
        self._surface.set_colorkey(BACKGROUND_COLOR)
        self._surface.fill(color)
        self.speed = 0.3
        self.ang_speed = 0.3
        self.spin_speed = 2
        self._pose = {
            "x": initial_pos[0],
            "y": initial_pos[1],
            "orientation": orientation,
        }

    def get_pos(self) -> Tuple:
        return self._pose.get("x"), self._pose.get("y")

    def get_orientation(self) -> float:
        return self._pose.get("orientation")

    def get_pose(self) -> Tuple:
        return self.get_pos(), self.get_orientation()

    def get_sprite(self) -> Surface:
        return self._surface

    def get_sprite_pos(self) -> Tuple[float, float]:
        return (
            self.get_pos()[0] - self.size[0] / 2,
            self.get_pos()[1] + self.size[1] / 2,
        )
    
    def update(self, action):
        pose_updates = self.__next_pose(action)
        
        for k in self._pose.keys():
            update = pose_updates.get(k)
            if isinstance(update, float):
                self._pose.update({k: update})

    def __next_pose(self, action) -> Dict[str,Optional[float]]:
        rotate, forward, spin = action
        if spin:
            return {
                "orientation": (self._pose.get("orientation") - self.spin_speed) % 360,
                "x": None,
                "y": None,
            }
        else:
            return {
                "orientation": (self._pose.get("orientation") - rotate * self.ang_speed) % 360,
                "x": self._pose.get("x")
                + math.cos(self._pose.get("orientation") * math.pi / 180) * self.speed * forward,
                "y": self._pose.get("y")
                + math.sin(self._pose.get("orientation") * math.pi / 180) * self.speed * forward,
            }

