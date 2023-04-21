from typing import Tuple
from math import radians, cos, sin
import pygame
from pygame.colordict import THECOLORS as colors
from game_elements.field import LEFT_FRONT_GOAL_X
from utils.agent_actions import Action
from utils.configs import SAMPLE_TIME
from game_elements.abstract_element import AbstractElement
from decision_making.abstract_policy import AbstractBehaviour
from world_state import WorldState

PLAYER_SPIN_COUNTDOWN = 200
PLAYER_LINEAR_SPEED = 0.1
PLAYER_ANGULAR_SPEED = 50
PLAYER_SPIN_SPEED = 100
PLAYER_SIDE = 0.075
PLAYER_SIZE = (PLAYER_SIDE, PLAYER_SIDE)


class Player(AbstractElement):
    def __init__(
        self,
        initial_pos: Tuple = (LEFT_FRONT_GOAL_X / 2, 0),
        orientation: float = 0,
        color: pygame.color = colors.get("white"),
        behaviour: AbstractBehaviour = AbstractBehaviour(),
    ):
        super().__init__(initial_pos=initial_pos, orientation=orientation, vel=0, size=PLAYER_SIZE)
        self._surface.set_colorkey(colors.get("black"))
        self._surface.fill(color)
        self.behaviour = behaviour
        self.spin_count = 0

    def update(self, world_state: WorldState):
        restart_spin = False
        if self.__should_spin_in_delay__():
            action = Action(spin=1)
        else:
            action = self.behaviour.get_action(world_state)
            if action.spin:
                restart_spin = True
        self.__update_spin_count__(restart_spin)

        pose_updates = self.__next_pose__(action)
        if self.__is_valid_update__(pose_updates):
            self._x, self._y, self._orientation, self._vel = pose_updates

    def __next_pose__(self, action: Action) -> Tuple[float]:
        if action.spin:
            new_orientation = (self._orientation - PLAYER_SPIN_SPEED * SAMPLE_TIME) % 360
            new_vel = 0
            return (self._x, self._y, new_orientation, new_vel)
        else:
            new_orientation = (self._orientation - action.rotate * PLAYER_ANGULAR_SPEED * SAMPLE_TIME) % 360
            return (
                self._x + cos(radians(self._orientation)) * PLAYER_LINEAR_SPEED * SAMPLE_TIME * action.forward,
                self._y + sin(radians(self._orientation)) * PLAYER_LINEAR_SPEED * SAMPLE_TIME * action.forward,
                new_orientation,
                PLAYER_LINEAR_SPEED * action.forward,
            )

    def __on_rebound__(self):
        pass

    def __should_spin_in_delay__(self) -> bool:
        if self.spin_count and self.spin_count < PLAYER_SPIN_COUNTDOWN:
            return True
        return False

    def __update_spin_count__(self, restart_spin: bool) -> None:
        if restart_spin or self.spin_count >= PLAYER_SPIN_COUNTDOWN:
            self.spin_count = 0
        if restart_spin or (self.spin_count and self.spin_count < PLAYER_SPIN_COUNTDOWN):
            self.spin_count += 1