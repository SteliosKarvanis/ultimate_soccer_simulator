from typing import Dict
import pygame
from pygame import Surface
from pygame.sprite import Group
from utils.types import GameElement
from typing import Tuple, Optional, List
from constants import *
import math
from utils.agent_actions import Action
from decision_making.abstract_policy import AbstractBehaviour

class Player(pygame.sprite.Sprite, GameElement):
    def __init__(
        self, coordinate_conversion, initial_pos: Tuple = (0, 0), orientation: float = 0, color:pygame.color = colors.get("white"), scale=1, behaviour: AbstractBehaviour = AbstractBehaviour(),
    ):
        super().__init__()
        self.size = (5, 5)
        self._surface = Surface((self.size[0] * scale, self.size[1] * scale))
        self._surface.set_colorkey(colors.get("black"))
        self._surface.fill(color)
        self.speed = 0.3
        self.ang_speed = 0.7
        self.spin_speed= 2
        self._x, self._y = initial_pos
        self._orientation = orientation
        self.coordinate_convert = coordinate_conversion
        self.behaviour = behaviour

    def get_sprite(self) -> Surface:
        return self._surface
    
    def update(self, boundary: Surface, elements: Group, world_state: Dict):
        action = self.behaviour.get_action(world_state)
        pose_updates = self.__next_pose(action)
        
        updated_values = []
        for i, update in enumerate(pose_updates):
            if not isinstance(update, float):
                updated_values.append(self.get_pose()[i])
            else:
                updated_values.append(update)

        if self.__is_valid_update__(updated_values, boundary, elements):
            self._orientation, self._x, self._y = tuple(updated_values)

    def __next_pose(self, action: Action) -> Tuple[Optional[float]]:
        if action.spin:
            return ((self._orientation - self.spin_speed) % 360, None, None)
        else:
            return (
                (self._orientation - action.rotate * self.ang_speed) % 360,
                self._x + math.cos(self._orientation * math.pi / 180) * self.speed * action.forward,
                self._y + math.sin(self._orientation * math.pi / 180) * self.speed * action.forward
                )
        
    def __is_valid_update__(self, updates: List[float], boundary: Surface, elements: Group)-> bool:
        new_sprite = pygame.transform.rotate(self._surface, updates[0])
        new_rect = new_sprite.get_rect()
        new_rect.center = self.coordinate_convert((updates[1], updates[2]))
        return boundary.get_rect().contains(new_rect)

