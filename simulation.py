import pygame
from pygame import Surface
from typing import Tuple
from GUI.player import Player
from GUI.ball import Ball
from GUI.scoreboard import ScoreBoard
from pygame.colordict import THECOLORS as colors
from decision_making.manual_policy import (
    ManualBehaviour,
)
from decision_making.FSM.fsm_policy import FSM
from utils.configs import (
    Configuration,
    SimulConfig,
)
from utils.types import GameElement
from GUI.field import FIELD_POINTS
from world_state import WorldState
from pygame.math import Vector2

MARGIN = 40
LINE_THICKNESS = 10


class Simulation:
    def __init__(
        self,
        config: Configuration,
        surface: Surface,
    ) -> None:
        self.configs = SimulConfig.generate_from_config(config)
        self.field = surface
        self.game_elements = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.FPS = self.configs.FPS
        self.ally = Player(
            self.players,
            self.game_elements,
            color=colors.get("darkblue"),
            behaviour=ManualBehaviour(),
        )
        self.opponent = Player(
            self.players,
            self.game_elements,
            color=colors.get("darkred"),
            initial_pos=(300, 0),
            behaviour=FSM(),
            orientation=180,
        )
        self.ball = Ball(self.players, self.game_elements)
        self.scoreboard = ScoreBoard(self.configs.scoreboard_height)
        self.clock = pygame.time.Clock()
        self.clock.tick(self.FPS)
        self.lines = self.draw_field()

    def update(self):
        self.ally.update(self.get_state())
        self.opponent.update(self.get_state())
        goal_state = self.ball.update()
        # if goal_state != "None":
        # self.scoreboard.update(character=goal_state, frame_height=self.configs.scoreboard_height)

    def draw(self):
        self.draw_field()
        self.__draw_elements__(self.game_elements)
        self.scoreboard.draw(self.field.get_abs_parent(), self.clock.tick())

    def get_state(self) -> WorldState:
        return WorldState(
            player_pos=self.ally.get_pos(),
            player_orientation=self.ally.get_orientation(),
            opponent_pos=self.opponent.get_pos(),
            opponent_orientation=self.opponent.get_orientation(),
            ball_pos=self.ball.get_pos(),
        )

    def __draw_elements__(
        self,
        group: pygame.sprite.Group,
    ) -> Surface:
        for sprite in group.sprites():
            self.__draw_element__(sprite)

    def __draw_element__(
        self,
        element: GameElement,
    ) -> Surface:
        sprite = element.get_sprite()
        rect = sprite.get_rect()
        rect.center = self.field_to_pix_coord(element.get_pos())
        self.field.get_parent().blit(source=sprite, dest=rect)

    def field_to_pix_coord(self, point: Vector2) -> Tuple[int, int]:
        point = [point[0] + self.get_field_center()[0], self.get_field_center()[1] - point[1]]
        return point

    def get_field_center(self) -> Vector2:
        center = self.field.get_rect().center
        return Vector2(center[0], center[1])

    def draw_field(self) -> pygame.Rect:
        field_points = [Vector2(self.field_to_pix_coord(x)) for x in FIELD_POINTS]
        return pygame.draw.lines(
            surface=self.field.get_parent(),
            color=pygame.Color("white"),
            closed=True,
            points=field_points,
            width=LINE_THICKNESS,
        )
