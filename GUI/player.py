import pygame
from utils.types import GameElement, colors, CollisionType
from typing import Tuple
import math
from utils.agent_actions import Action
from decision_making.abstract_policy import AbstractBehaviour
from utils.configs import SAMPLE_TIME
from world_state import WorldState
from enum import Enum

PLAYER_LINEAR_SPEED = 100
PLAYER_ANGULAR_SPEED = 50
PLAYER_SIDE = 40
PLAYER_SIZE = (PLAYER_SIDE, PLAYER_SIDE)


class PlayerState(Enum):
    PLAYING = 1
    ON_REBOUND = 2
    ON_FEINT = 3
    ON_SPIN = 4


class Player(GameElement):
    def __init__(
        self,
        *groups,
        initial_pos=(-300, 0),
        color: pygame.color = colors.get("white"),
        **kwargs,
    ):
        self.ang_speed = PLAYER_ANGULAR_SPEED
        kwargs.update({"_x": initial_pos[0], "_y": initial_pos[1]})
        super().__init__(*groups, color=color, size=PLAYER_SIZE, inertia=100, **kwargs)
        self._vel = PLAYER_LINEAR_SPEED
        self._spin_speed = 200
        self.behaviour = kwargs.get("behaviour", AbstractBehaviour())
        self.spin_count = 0
        self.state = PlayerState.PLAYING
        self.rebound_count = 0
        self.rebound_action = Action()
        self.previous_forward = 1
        self.spin_action = Action(spin=1)

    def update(self, world_state: WorldState):
        action = self.behaviour.get_action(world_state)
        pose_updates = self.__next_pose__(action)
        match self.__get_update__(pose_updates):

            case CollisionType.NONE | CollisionType.BALL_PLAYER:
                pose_updates = self.__player_state_FSM__(action, pose_updates)

            case CollisionType.WITH_SCENERY:
                if self.state == PlayerState.ON_REBOUND:
                    pose_updates = (0,0,0)
                else:
                    self.state = PlayerState.ON_REBOUND
                    self.rebound_count = 25
                    self.rebound_action = Action(rotate=-action.rotate, forward=-action.forward, spin=-action.spin)
                    pose_updates = self.__next_pose__(self.rebound_action)
                    if self.rebound_action.forward != 0:
                        self.previous_forward = self.rebound_action.forward

            case CollisionType.OF_PLAYERS:
                self.state = PlayerState.ON_FEINT
                self.rebound_count = 10
                self.rebound_action = Action(rotate=-action.rotate, forward=-action.forward, spin=-action.spin)
                pose_updates = self.__next_pose__(self.rebound_action)
                if self.rebound_action.forward != 0:
                    self.previous_forward = self.rebound_action.forward

        self._orientation, self._x, self._y = pose_updates
        self._sprite = pygame.transform.rotate(self.image, self._orientation)
        self.mask = pygame.mask.from_surface(self._sprite)
        self.rect = self._sprite.get_rect()
        self.rect.center = self._x, self._y


    def __player_state_FSM__(self, action: Action, prev_updates: Tuple[float])->Tuple[float]:
        match self.state:
            case PlayerState.ON_REBOUND | PlayerState.ON_FEINT:
                if self.rebound_count <= 0:
                    self.state = PlayerState.PLAYING
                    if action.forward != 0:
                        self.previous_forward = action.forward

                else:
                    self.rebound_count -= 1
                    return self.__next_pose__(self.rebound_action)

            case PlayerState.ON_SPIN:
                if self.spin_count <= 0:
                    self.state = PlayerState.PLAYING
                    self.spin_action = Action(spin=1)
                else:
                    self.spin_count -= 1
                    print(self._orientation)
                    return self.__next_pose__(self.spin_action)

            case PlayerState.PLAYING:
                if action.forward != 0:
                    self.previous_forward = action.forward

        return prev_updates

    def __next_pose__(self, action: Action) -> Tuple[float]:
        if action.spin != 0 or self.state == PlayerState.ON_SPIN:
            if self.state != PlayerState.ON_SPIN:
                if self.state == PlayerState.ON_REBOUND:
                    self.spin_action = self.rebound_action
                self.state = PlayerState.ON_SPIN
                self.spin_count = 30
            return (
                (self._orientation - self._spin_speed * SAMPLE_TIME * action.spin) % 360, #spin is only ever negative when rebounding
                self._x,
                self._y,
            )
        else:
            return (
                (self._orientation - action.rotate * self.ang_speed * SAMPLE_TIME + 180 * (action.forward * self.previous_forward < 0)) % 360,
                self._x + math.cos(self._orientation * math.pi / 180) * self._vel * SAMPLE_TIME * (action.forward != 0),
                self._y + math.sin(self._orientation * math.pi / 180) * self._vel * SAMPLE_TIME * (action.forward != 0),
            )
