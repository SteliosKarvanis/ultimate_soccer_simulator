from typing import Tuple
from math import radians, cos, sin
import pygame
from pygame.math import Vector3
from game_elements.field import LEFT_FRONT_GOAL_X
from utils.agent_actions import Action
from utils.configs import SAMPLE_TIME
from game_elements.abstract_element import AbstractElement
from decision_making.abstract_policy import AbstractBehaviour
from world_state import WorldState
from utils.collision_handler import CollisionHandler

PLAYER_SPIN_COUNTDOWN = 5
PLAYER_LINEAR_SPEED = 0.25
PLAYER_SPIN_SPEED = 1000
PLAYER_SIDE = 0.07
PLAYER_SIZE = (PLAYER_SIDE, PLAYER_SIDE)


class Player(AbstractElement):
    def __init__(
        self,
        asset_path: str,
        initial_pos: Tuple = (LEFT_FRONT_GOAL_X / 3, 0),
        orientation: float = 0,
        behaviour: AbstractBehaviour = AbstractBehaviour(),
    ):
        super().__init__(initial_pos=initial_pos, orientation=orientation, vel=0, size=PLAYER_SIZE)
        self._surface = pygame.image.load(asset_path)
        self.behaviour = behaviour
        self.spin_count = 0
        self.rebound_action = Action()
        self.rebound_count = 0
        self.last_moving_action = Action()
        self.last_valid_pose = self.get_state()
        self.base_vel = PLAYER_LINEAR_SPEED
        self.angular_speed = self.base_vel*500

    def set_pose(self, collision_handler: CollisionHandler, pose: Vector3 = (LEFT_FRONT_GOAL_X / 3, 0, 0)):
        self._x, self._y, self._orientation = pose
        collision_handler.update_element_sprite(self)

    def update(self, world_state: WorldState, collision_handler: CollisionHandler):
        restart_spin = False
        if self.__should_spin_in_delay__():
            action = Action(spin=1)
        else:
            action = self.behaviour.get_action(world_state)
            if action.spin:
                restart_spin = True
        self.__update_spin_count__(restart_spin)

        if self.rebound_count > 0:
            self.__update_state__(self.__next_pose__(self.rebound_action), collision_handler)
            self.rebound_count -= 1
        else:
            pose_updates = self.__next_pose__(action)
            if not self.__is_valid_update__(pose_updates, collision_handler):
                self.__update_state__(self.last_valid_pose, collision_handler)
                if action.forward != 0:
                    self.last_moving_action = action
                self.rebound_action = Action(-self.last_moving_action.rotate, -self.last_moving_action.forward, 0)
                self.rebound_count = 40

            else:
                self.last_valid_pose = pose_updates
                if action.forward != 0:
                    self.last_moving_action = action
                self.__update_state__(pose_updates, collision_handler)
            

    def __is_valid_update__(self, updates: Tuple[float, float, float, float], collision_handler: CollisionHandler) -> bool:
        return super().__is_valid_update__(updates) and not collision_handler.check_collision(self)
    
    def __update_state__(self, updates, collision_handler: CollisionHandler):
        self._x, self._y, self._orientation, self._vel = updates
        collision_handler.update_element_sprite(self)

    def __next_pose__(self, action: Action) -> Tuple[float]:
        if action.spin:
            new_orientation = (self._orientation - PLAYER_SPIN_SPEED * SAMPLE_TIME) % 360
            new_vel = 0
            return (self._x, self._y, new_orientation, new_vel)
        else:
            new_orientation = (self._orientation - action.rotate * self.angular_speed * SAMPLE_TIME) % 360
            return (
                self._x + cos(radians(self._orientation)) * self._vel * SAMPLE_TIME,
                self._y + sin(radians(self._orientation)) * self._vel * SAMPLE_TIME,
                new_orientation,
                self.base_vel * action.forward,
            )

    def __should_spin_in_delay__(self) -> bool:
        if self.spin_count and self.spin_count < PLAYER_SPIN_COUNTDOWN:
            return True
        return False

    def __update_spin_count__(self, restart_spin: bool) -> None:
        if restart_spin or self.spin_count >= PLAYER_SPIN_COUNTDOWN:
            self.spin_count = 0
        if restart_spin or (self.spin_count and self.spin_count < PLAYER_SPIN_COUNTDOWN):
            self.spin_count += 1
