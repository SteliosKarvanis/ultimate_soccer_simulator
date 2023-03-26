import pygame 
from constants import *
from typing import Dict
from utils.agent_actions import Action
from decision_making.abstract_policy import AbstractBehaviour

class ManualBehaviour(AbstractBehaviour):
    def __init__(self) -> None:
        super().__init__()
        self.spin_count = 0

    def get_action(self, world_state: Dict) -> Action:
        action = Action()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or self.spin_count:
            if keys[pygame.K_SPACE]:
                self.spin_count = 0
            self.spin_count += 1
            if self.spin_count >= PLAYER_SPIN_COUNTDOWN:
                self.spin_count = 0
        
        if keys[pygame.K_LEFT]:
            action.rotate -= 1
        if keys[pygame.K_RIGHT]:
            action.rotate += 1
        if keys[pygame.K_UP]:
            action.forward += 1
        if keys[pygame.K_DOWN]:
            action.forward -= 1
        if self.spin_count:
            action.spin = 1
            
        return action