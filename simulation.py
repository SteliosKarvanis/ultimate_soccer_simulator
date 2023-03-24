import math
import pygame
from pygame import Surface
from typing import Dict, Tuple
from GUI.player import Player
from GUI.ball import Ball
from GUI.scoreboard import ScoreBoard
from constants import *
from decision_making.manual_policy import ManualBehaviour
from utils.configs import Configuration, SimulConfig

class Point(Tuple[float,float]):
    def __init__(self) -> None:
        super().__init__()

class Simulation:
    def __init__(self, config: Configuration) -> None:
        self.configs = SimulConfig.generate_from_config(config)
        self.FPS = self.configs.FPS
        self.field_coordinate_scale = self.configs.field_size[0]/100
        self.ally = Player(scale=self.field_coordinate_scale)
        self.opponent = Player(scale=self.field_coordinate_scale)
        self.ball = Ball()
        self.ally_behaviour = ManualBehaviour()
        self.scoreboard = ScoreBoard(self.configs.scoreboard_height)
        self.clock = pygame.time.Clock()
        self.clock.tick(self.FPS)

    def update(self):
        ally_action = self.ally_behaviour.get_action(self.get_state())
        self.ally.update(ally_action)
        #self.opponent.update(None)
        self.ball.update(None)
    
    def draw(self, screen: Surface):
        screen = self.__draw_player__(screen, self.ally)
        screen = self.__draw_player__(screen, self.opponent)
        screen = self.ball.draw(screen)
        screen = self.scoreboard.draw(screen, self.clock.tick())
        return screen

    def get_state(self) -> Dict:
        return {
            "player_pose":self.ally.get_pose(),
            "opponent_pose":self.opponent.get_pose(),
            "ball_pos":self.ball.pos,
            "ball_vel":self.ball.vel,
            "score":self.scoreboard.get_score(),
        }
    
    def __draw_player__(self, screen: Surface, player: Player)-> Surface:
        updated_sprite = pygame.transform.rotate(player.get_sprite(), player.get_orientation())
        rect = updated_sprite.get_rect()
        rect.center = self.__c_to_p__(player.get_sprite_pos())
        screen.blit(source=updated_sprite, dest=rect)
        return screen

    def __c_to_p__ (self, point: Point) -> Tuple[int, int]:
        pixels = [0, 0]
        w, h = self.configs.field_size
        offset = self.configs.status_bar_height
        pixels[0] = w/2 + point[0]*self.field_coordinate_scale
        pixels[1] = offset + h/2 - point[1]*self.field_coordinate_scale
        return tuple(pixels)
