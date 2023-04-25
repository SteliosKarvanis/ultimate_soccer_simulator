import pygame
from typing import Dict
from utils.agent_actions import Action
from decision_making.abstract_policy import AbstractBehaviour
from world_state import WorldState


class ManualBehaviour(AbstractBehaviour):
    def __init__(self) -> None:
        super().__init__()

    def get_action(self, worldstate: WorldState) -> Action:
        action = Action()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            action.spin = 1
        else:
            if keys[pygame.K_LEFT]:
                action.rotate -= 1
            elif keys[pygame.K_RIGHT]:
                action.rotate += 1
            if keys[pygame.K_UP]:
                action.forward += 1
            elif keys[pygame.K_DOWN]:
                action.forward -= 1
        return action
