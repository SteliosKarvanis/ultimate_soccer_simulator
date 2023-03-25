import math
import pygame
from typing import Dict
from GUI.player import Player
from GUI.ball import Ball
from GUI.scoreboard import ScoreBoard
from constants import *
from decision_making.manual_policy import ManualBehaviour
from decision_making.FSM.fsm_policy import FSM

class Simulation:
    def __init__(self) -> None:
        self.ally = Player()
        self.opponent = Player()
        self.ball = Ball()
        self.ally_behaviour = ManualBehaviour()
        self.opponent_behaviour = FSM()
        self.scoreboard = ScoreBoard()
        self.clock = pygame.time.Clock()
        self.clock.tick()
    def update(self):
        ally_action = self.ally_behaviour.get_action(self.get_state())
        opp_action = self.opponent_behaviour.get_action(self.get_state())
        self.ally.update(ally_action)
        self.opponent.update(opp_action)
        self.ball.update(None)
    
    def draw(self, screen):
        screen = self.ally.draw(screen)
        screen = self.opponent.draw(screen)
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
        