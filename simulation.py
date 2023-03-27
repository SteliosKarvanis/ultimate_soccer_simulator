import math
import pygame
from pygame import Surface
from typing import Dict, Tuple
from GUI.player import Player
from GUI.ball import Ball
from GUI.scoreboard import ScoreBoard
from pygame.colordict import THECOLORS as colors
from decision_making.manual_policy import ManualBehaviour
from decision_making.FSM.fsm_policy import FSM
from utils.configs import Configuration, SimulConfig
from utils.types import Point, GameElement
from GUI.field import draw_field


class Simulation:
    def __init__(self, config: Configuration, boundary: Surface) -> None:
        self.configs = SimulConfig.generate_from_config(config)
        self.boundary = boundary
        self.FPS = self.configs.FPS
        self.field_coordinate_scale = self.configs.field_size[0] / 100
        self.ally = Player(
            self.__to_boundary_coord__,
            scale=self.field_coordinate_scale,
            color=colors.get("darkblue"),
            behaviour=ManualBehaviour(),
        )
        self.opponent = Player(
            self.__to_boundary_coord__,
            scale=self.field_coordinate_scale,
            color=colors.get("darkred"),
            behaviour=FSM(),
        )
        self.ball = Ball()
        self.game_elements = pygame.sprite.Group(self.ally, self.opponent, self.ball)
        self.scoreboard = ScoreBoard(self.configs.scoreboard_height)
        self.clock = pygame.time.Clock()
        self.clock.tick(self.FPS)

    def update(self):
        self.ally.update(self.boundary, self.game_elements, self.get_state())
        self.opponent.update(self.boundary, self.game_elements, self.get_state())
        self.ball.update(None)

    def draw(self, screen: Surface):
        screen = self.__draw_elements__(screen, self.game_elements)
        screen = self.scoreboard.draw(screen, self.clock.tick())
        screen = draw_field(screen, (640, 436))
        return screen

    def get_state(self) -> Dict:
        return {
            "player_pose": self.ally.get_pose(),
            "opponent_pose": self.opponent.get_pose(),
            "ball_pos": self.ball.get_pos(),
            "ball_vel": self.ball._vel,
            "score": self.scoreboard.get_score(),
        }

    def __draw_elements__(self, screen: Surface, group: pygame.sprite.Group) -> Surface:
        for sprite in group.sprites():
            screen = self.__draw_element__(screen, sprite)
        return screen

    def __draw_element__(self, screen: Surface, element: GameElement) -> Surface:
        sprite = pygame.transform.rotate(element.get_sprite(), element.get_orientation())
        rect = sprite.get_rect()
        rect.center = self.__boundary_to_screen__(element.get_pos())
        screen.blit(source=sprite, dest=rect)
        return screen

    def __boundary_to_screen__(self, point: Point) -> Point:
        pixels = [0, 0]
        boundary_coord = self.__to_boundary_coord__(point)
        offset = self.configs.status_bar_height
        pixels[0] = boundary_coord[0]
        pixels[1] = offset + boundary_coord[1]
        return tuple(pixels)

    def __to_boundary_coord__(self, point: Point) -> Point:
        pixels = [0, 0]
        w, h = self.configs.field_size
        pixels[0] = w / 2 + point[0] * self.field_coordinate_scale
        pixels[1] = h / 2 - point[1] * self.field_coordinate_scale
        return tuple(pixels)
