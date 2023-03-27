from typing import Dict
import pygame
from pygame import Surface
from pygame.sprite import Group
from utils.types import GameElement
from typing import Tuple, Optional, List
from pygame.colordict import THECOLORS as colors
import math
from utils.agent_actions import Action
from decision_making.abstract_policy import AbstractBehaviour
from utils.configs import SAMPLE_TIME

PLAYER_SPIN_COUNTDOWN = 200
PLAYER_LINEAR_SPEED = 3
PLAYER_ANGULAR_SPEED = 35
PLAYER_SPIN_SPEED = 100
PLAYER_SIZE = (4, 4)


class Player(pygame.sprite.Sprite, GameElement):
    def __init__(
        self,
        coordinate_conversion,
        initial_pos: Tuple = (0, 0),
        orientation: float = 0,
        color: pygame.color = colors.get("white"),
        scale=1,
        behaviour: AbstractBehaviour = AbstractBehaviour(),
    ):
        super().__init__()
        self.size = PLAYER_SIZE
        self._surface = Surface((self.size[0] * scale, self.size[1] * scale))
        self._surface.set_colorkey(colors.get("black"))
        self._surface.fill(color)
        self.speed = PLAYER_LINEAR_SPEED
        self.ang_speed = PLAYER_ANGULAR_SPEED
        self.spin_speed = PLAYER_SPIN_SPEED
        self._x, self._y = initial_pos
        self._orientation = orientation
        self.coordinate_convert = coordinate_conversion
        self.behaviour = behaviour
        self.spin_count = 0

    def get_sprite(self) -> Surface:
        return self._surface

    def update(self, boundary: Surface, elements: Group, world_state: Dict):
        restart_spin = False
        if self.__should_spin_in_delay():
            action = Action(spin=1)
        else:
            action = self.behaviour.get_action(world_state)
            if action.spin:
                restart_spin = True
        self.__update_spin_count(restart_spin)

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
            return ((self._orientation - self.spin_speed * SAMPLE_TIME) % 360, None, None)
        else:
            return (
                (self._orientation - action.rotate * self.ang_speed * SAMPLE_TIME) % 360,
                self._x + math.cos(self._orientation * math.pi / 180) * self.speed  * SAMPLE_TIME * action.forward,
                self._y + math.sin(self._orientation * math.pi / 180) * self.speed  * SAMPLE_TIME * action.forward,
            )

    def __is_valid_update__(self, updates: List[float], boundary: Surface, elements: Group) -> bool:
        new_sprite = pygame.transform.rotate(self._surface, updates[0])
        new_rect = new_sprite.get_rect()
        new_rect.center = self.coordinate_convert((updates[1], updates[2]))
        return boundary.get_rect().contains(new_rect)

    def __should_spin_in_delay(self) -> bool:
        if self.spin_count and self.spin_count < PLAYER_SPIN_COUNTDOWN:
            return True
        return False

    def __update_spin_count(self, restart_spin: bool) -> None:
        if restart_spin or self.spin_count >= PLAYER_SPIN_COUNTDOWN:
            self.spin_count = 0
        if restart_spin or (self.spin_count and self.spin_count < PLAYER_SPIN_COUNTDOWN):
            self.spin_count += 1
