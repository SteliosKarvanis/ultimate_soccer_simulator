from typing import Tuple, List
from math import radians, cos, sin
import pygame
from pygame.sprite import Sprite, Group
from pygame.colordict import THECOLORS as colors
from game_elements.field import LEFT_FRONT_GOAL_X
from utils.agent_actions import Action
from utils.configs import SAMPLE_TIME
from game_elements.abstract_element import AbstractElement
from decision_making.abstract_policy import AbstractBehaviour
from world_state import WorldState

PLAYER_SPIN_COUNTDOWN = 200
PLAYER_LINEAR_SPEED = 0.25
PLAYER_ANGULAR_SPEED = 500*PLAYER_LINEAR_SPEED
PLAYER_SPIN_SPEED = 100
PLAYER_SIDE = 0.075
PLAYER_SIZE = (PLAYER_SIDE, PLAYER_SIDE)


class Player(AbstractElement):
    def __init__(
        self,
        group: Group,
        scale,
        initial_pos: Tuple = (LEFT_FRONT_GOAL_X / 2, 0),
        orientation: float = 0,
        color: pygame.color = colors.get("white"),
        behaviour: AbstractBehaviour = AbstractBehaviour(),
    ):
        super().__init__(initial_pos=initial_pos, orientation=orientation, vel=0, size=PLAYER_SIZE)
        self.add(group)
        self._surface.set_colorkey(colors.get("black"))
        self._surface.fill(color)
        self.behaviour = behaviour
        self.spin_count = 0
        self.scale = scale
        self._sprite = pygame.transform.scale(self._surface, self.scale(self.size))
        self._sprite = pygame.transform.rotate(self._sprite, self._orientation)
        self.mask = pygame.mask.from_surface(self._surface)
        self.rect = self._sprite.get_rect()
        self.rect.center = self.scale((self._x, self._y))
        self.rebound_action = Action()
        self.rebound_count = 0
        self.last_moving_action = Action()
        self.last_valid_pose = self.get_state()
        self.base_vel = PLAYER_LINEAR_SPEED

    def update(self, world_state: WorldState):
        restart_spin = False
        if self.__should_spin_in_delay__():
            action = Action(spin=1)
        else:
            action = self.behaviour.get_action(world_state)
            if action.spin:
                restart_spin = True
        self.__update_spin_count__(restart_spin)

        if self.rebound_count > 0:
            self.__update_state__(self.__next_pose__(self.rebound_action))
            self.rebound_count -= 1
        else:
            pose_updates = self.__next_pose__(action)
            if not self.__is_valid_update__(pose_updates):
                self.__update_state__(self.last_valid_pose)
                if action.forward != 0:
                    self.last_moving_action = action
                self.rebound_action = Action(-self.last_moving_action.rotate, -self.last_moving_action.forward, 0)
                self.rebound_count = 40

            else:
                self.last_valid_pose = pose_updates
                if action.forward != 0:
                    self.last_moving_action = action
                self.__update_state__(pose_updates)
            

    def __is_valid_update__(self, updates: Tuple[float, float, float, float]) -> bool:
        return super().__is_valid_update__(updates) and self.check_collision()
    
    def __update_state__(self, updates):
        self._x, self._y, self._orientation, self._vel = updates
        self._sprite = pygame.transform.scale(self._surface, self.scale(self.size))
        self._sprite = pygame.transform.rotate(self._sprite, self._orientation)
        self.mask = pygame.mask.from_surface(self._sprite)
        self.rect = self._sprite.get_rect()
        self.rect.center = self.scale((self._x, self._y))

    def __next_pose__(self, action: Action) -> Tuple[float]:
        if action.spin:
            new_orientation = (self._orientation - PLAYER_SPIN_SPEED * SAMPLE_TIME) % 360
            new_vel = 0
            return (self._x, self._y, new_orientation, new_vel)
        else:
            new_orientation = (self._orientation - action.rotate * PLAYER_ANGULAR_SPEED * SAMPLE_TIME) % 360
            return (
                self._x + cos(radians(self._orientation)) * self._vel * SAMPLE_TIME,
                self._y + sin(radians(self._orientation)) * self._vel * SAMPLE_TIME,
                new_orientation,
                self.base_vel * action.forward,
            )

    def check_collision(self) -> bool:
        for group in self.groups():
            if len(group) == 2:
                for element in Player.group_collide(self, group):
                    return False
        return True

    @staticmethod
    def group_collide(sprite: Sprite, group: Group) -> List[Sprite]:
        return [element for element in pygame.sprite.spritecollide(sprite, group, False, collided=Player.collision_handler)]

    @staticmethod
    def collision_handler(sprite1: Sprite, sprite2: Sprite):
        collision_point = pygame.sprite.collide_mask(sprite1, sprite2)
        return collision_point != None and sprite1 != sprite2

    def __should_spin_in_delay__(self) -> bool:
        if self.spin_count and self.spin_count < PLAYER_SPIN_COUNTDOWN:
            return True
        return False

    def __update_spin_count__(self, restart_spin: bool) -> None:
        if restart_spin or self.spin_count >= PLAYER_SPIN_COUNTDOWN:
            self.spin_count = 0
        if restart_spin or (self.spin_count and self.spin_count < PLAYER_SPIN_COUNTDOWN):
            self.spin_count += 1
