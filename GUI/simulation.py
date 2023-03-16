import math
import pygame
from GUI.player import Player
from GUI.ball import Ball
from constants import *
from decision_making.manual import ManualBehaviour

class Simulation:
    def __init__(self) -> None:
        self.score = (0, 0)
        self.ally = Player()
        self.opponent = Player()
        self.ball = Ball()
        self.ally_behaviour = ManualBehaviour()

    def update(self):
        opp_action = (0, 0, 0)
        ally_action = self.ally_behaviour.get_action(None)
        ball_action = None
        self.ally.update(ally_action)
        self.opponent.update(opp_action)
        self.ball.update(ball_action)
    
    def draw(self, screen):
        screen = self.ally.draw(screen)
        screen = self.opponent.draw(screen)
        screen = self.ball.draw(screen)
        return screen
