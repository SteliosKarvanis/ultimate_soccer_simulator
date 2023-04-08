import pygame
from pygame import Surface
from utils.types import GameElement
from typing import Tuple
from pygame.colordict import THECOLORS as colors
import math
from utils.agent_actions import Action
from decision_making.abstract_policy import AbstractBehaviour
from utils.configs import SAMPLE_TIME
from world_state import WorldState

PLAYER_LINEAR_SPEED = 100
PLAYER_ANGULAR_SPEED = 50
PLAYER_SIDE = 40
PLAYER_SIZE = (PLAYER_SIDE, PLAYER_SIDE)



class Player(GameElement):
    def __init__(
        self,
        initial_pos: Tuple = (-300, 0),
        orientation: float = 0,
        color: pygame.color = colors.get("white"),
        behaviour: AbstractBehaviour = AbstractBehaviour(),
        **kwargs
    ):
        super().__init__()
        self.size = PLAYER_SIZE
        self._surface = Surface(self.size)
        self._surface.set_colorkey(colors.get("black"))
        self._surface.fill(color)
        self.speed = PLAYER_LINEAR_SPEED
        self.ang_speed = PLAYER_ANGULAR_SPEED
        self._x, self._y = initial_pos
        self._orientation = orientation
        self.behaviour = behaviour
        self.spin_count = 0

    def get_surface(self) -> Surface:
        return self._surface

    def update(self, world_state: WorldState):
        action = self.behaviour.get_action(world_state)    

        pose_updates = self.__next_pose__(action)
        if self.__is_valid_update__(pose_updates):
            self._orientation, self._x, self._y = pose_updates

    def __next_pose__ (self, action: Action) -> Tuple[float]:
        if action.spin:
            return ((self._orientation - self.spin_speed * SAMPLE_TIME) % 360, self._x, self._y)
        else:
            return (
                (self._orientation - action.rotate * self.ang_speed * SAMPLE_TIME) % 360,
                self._x + math.cos(self._orientation * math.pi / 180) * self.speed * SAMPLE_TIME * action.forward,
                self._y + math.sin(self._orientation * math.pi / 180) * self.speed * SAMPLE_TIME * action.forward,
            )
        
    def __on_rebound__(self):
        pass