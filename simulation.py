from typing import Tuple
import pygame
from pygame import Surface
from pygame.math import Vector2
from pygame.colordict import THECOLORS as colors
from GUI.scoreboard import ScoreBoard
from game_elements.abstract_element import AbstractElement
from game_elements.field import FIELD_POINTS
from game_elements.player import Player
from game_elements.ball import Ball
from decision_making.manual_policy import ManualBehaviour
from decision_making.FSM.fsm_policy import FSM
from utils.configs import Configuration, SimulConfig
from world_state import WorldState

MARGIN = 40
LINE_THICKNESS = 10


class Simulation:
    def __init__(self, config: Configuration, surface: Surface) -> None:
        self.configs = SimulConfig.generate_from_config(config)
        self.surface = surface
        self.FPS = self.configs.FPS
        self.ally = Player(
            color=colors.get("darkblue"),
            behaviour=ManualBehaviour(),
        )
        self.opponent = Player(
            color=colors.get("darkred"),
            behaviour=FSM(),
        )
        self.ball = Ball()
        self.game_elements = pygame.sprite.Group(self.ally, self.opponent, self.ball)
        self.scoreboard = ScoreBoard(self.configs.scoreboard_height)
        self.clock = pygame.time.Clock()
        self.clock.tick(self.FPS)

    def update(self):
        self.ally.update(self.get_state())
        self.opponent.update(self.get_state())
        if not self.ball.collision_management(self.ally):
            l = self.ball.collision_management(self.opponent)
        goal_state = self.ball.update()
        if goal_state != "None":
            self.scoreboard.update(character=goal_state, frame_height=self.configs.scoreboard_height)

    def draw(self, screen: Surface) -> Surface:
        screen = self.draw_field(screen)
        screen = self.__draw_elements__(screen, self.game_elements)
        screen = self.scoreboard.draw(screen, self.clock.tick())
        return screen

    def get_state(self) -> WorldState:
        return WorldState(
            player_state=self.ally.get_state(),
            opponent_state=self.opponent.get_state(),
            ball_state=self.ball.get_state(),
        )

    def __draw_elements__(self, screen: Surface, group: pygame.sprite.Group) -> Surface:
        for sprite in group.sprites():
            screen = self.__draw_element__(screen, sprite)
        return screen

    def __draw_element__(self, screen: Surface, element: AbstractElement) -> Surface:
        sprite = pygame.transform.rotate(element.get_surface(), element.get_orientation())
        rect = sprite.get_rect()
        rect.center = self.field_to_pix_coord(element.get_pos())
        screen.blit(source=sprite, dest=rect)
        return screen

    def pix_to_field_coord(self, point: Vector2) -> Vector2:
        point[1] *= -1
        return point - self.get_field_center()

    def field_to_pix_coord(self, point: Vector2) -> Tuple[int, int]:
        point = point + self.get_field_center()
        point[1] *= -1
        return point

    def get_field_center(self) -> Vector2:
        center = self.surface.get_bounding_rect().center
        # TODO: fix the math behind the line below
        return Vector2(center[0], -center[1] - self.scoreboard.frame.get_height() / 2 - MARGIN)

    def draw_field(self, screen: Surface) -> Surface:
        field_points = [self.field_to_pix_coord(x) for x in FIELD_POINTS]
        pygame.draw.lines(
            surface=screen, color=pygame.Color("white"), closed=True, points=field_points, width=LINE_THICKNESS
        )
        return screen
