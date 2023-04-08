import pygame
from pygame import Surface
from utils.types import GameElement, colors
from typing import Tuple
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
        *args,
        initial_pos=(-300, 0),
        color: pygame.color = colors.get("white"),
        **kwargs
    ):
        self.ang_speed = PLAYER_ANGULAR_SPEED
        kwargs.update({"_x": initial_pos[0], "_y": initial_pos[1]})
        super().__init__(*args, size = PLAYER_SIZE, inertia = 100, **kwargs)
        self._surface.fill(color)
        self._vel = PLAYER_LINEAR_SPEED
        self.behaviour = kwargs.get('behaviour', AbstractBehaviour())
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
                self._x + math.cos(self._orientation * math.pi / 180) * self._vel * SAMPLE_TIME * action.forward,
                self._y + math.sin(self._orientation * math.pi / 180) * self._vel * SAMPLE_TIME * action.forward,
            )
        
    def __on_rebound__(self):
        pass