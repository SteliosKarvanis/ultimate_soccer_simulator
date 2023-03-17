import math
import pygame
from typing import Dict
from GUI.player import Player
from GUI.ball import Ball
from constants import *
from decision_making.manual_policy import ManualBehaviour

class Simulation:
    def __init__(self) -> None:
        self.score = (0, 0)
        self.ally = Player()
        self.opponent = Player()
        self.ball = Ball()
        self.ally_behaviour = ManualBehaviour()

    def update(self):
        ally_action = self.ally_behaviour.get_action(self.get_state())
        self.ally.update(ally_action)
        #self.opponent.update(None)
        self.ball.update(None)
    
    def draw(self, screen):
        screen = self.ally.draw(screen)
        screen = self.opponent.draw(screen)
        screen = self.ball.draw(screen)
        return screen

    def get_state(self) -> Dict:
        return {
            "player_pose":self.ally.get_pose(),
            "opponent_pose":self.opponent.get_pose(),
            "ball_pos":self.ball.pos,
            "ball_vel":self.ball.vel,
        }
        