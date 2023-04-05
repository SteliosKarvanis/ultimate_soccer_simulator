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

PLAYER_SPIN_COUNTDOWN = 200
PLAYER_LINEAR_SPEED = 30
PLAYER_ANGULAR_SPEED = 35
PLAYER_SPIN_SPEED = 100
PLAYER_SIDE = 40
PLAYER_SIZE = (PLAYER_SIDE, PLAYER_SIDE)


class Player(pygame.sprite.Sprite, GameElement):
    def __init__(
        self,
        initial_pos: Tuple = (-300, 0),
        orientation: float = 0,
        color: pygame.color = colors.get("white"),
        behaviour: AbstractBehaviour = AbstractBehaviour(),
    ):
        super().__init__()
        self.size = PLAYER_SIZE
        self._surface = Surface(self.size)
        self._surface.set_colorkey(colors.get("black"))
        self._surface.fill(color)
        self.speed = PLAYER_LINEAR_SPEED
        self.ang_speed = PLAYER_ANGULAR_SPEED
        self.spin_speed = PLAYER_SPIN_SPEED
        self._x, self._y = initial_pos
        self._orientation = orientation
        self.behaviour = behaviour
        self.spin_count = 0
        self.velocity_orientation = orientation
        self.vel = 0

    def update(self, world_state: WorldState):
        restart_spin = False
        if self.__should_spin_in_delay():
            action = Action(spin=1)
        else:
            action = self.behaviour.get_action(world_state)
            if action.spin:
                restart_spin = True
        self.__update_spin_count(restart_spin)

        pose_updates = self.__next_pose(action)
        if self.__is_valid_update__(pose_updates):
            self._orientation, self._x, self._y = pose_updates

    def __next_pose(self, action: Action) -> Tuple[float]:
        self.vel = abs(self.speed * action.forward)
        if action.spin:
            self.velocity_orientation = (self._orientation - self.spin_speed * SAMPLE_TIME) % 360
            return ((self._orientation - self.spin_speed * SAMPLE_TIME) % 360, self._x, self._y)
        else:
            if action.forward >= 0:
                self.velocity_orientation = (self._orientation - action.rotate * self.ang_speed * SAMPLE_TIME) % 360
            else:
                self.velocity_orientation = (
                    180 + self._orientation - action.rotate * self.ang_speed * SAMPLE_TIME
                ) % 360
            return (
                (self._orientation - action.rotate * self.ang_speed * SAMPLE_TIME) % 360,
                self._x + math.cos(self._orientation * math.pi / 180) * self.speed * SAMPLE_TIME * action.forward,
                self._y + math.sin(self._orientation * math.pi / 180) * self.speed * SAMPLE_TIME * action.forward,
            )

    def __should_spin_in_delay(self) -> bool:
        if self.spin_count and self.spin_count < PLAYER_SPIN_COUNTDOWN:
            return True
        return False

    def __update_spin_count(self, restart_spin: bool) -> None:
        if restart_spin or self.spin_count >= PLAYER_SPIN_COUNTDOWN:
            self.spin_count = 0
        if restart_spin or (self.spin_count and self.spin_count < PLAYER_SPIN_COUNTDOWN):
            self.spin_count += 1
