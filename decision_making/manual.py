import pygame 
from constants import *
import math
from typing import Tuple

class ManualBehaviour:
    def __init__(self) -> None:
        self.spin_count = 0

    def get_action(self, state) -> Tuple:
        rotate = 0
        forward = 0
        spin = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or self.spin_count:
            if keys[pygame.K_SPACE]:
                self.spin_count = 0
            self.spin_count += 1
            if self.spin_count >= PLAYER_SPIN_COUNTDOWN:
                self.spin_count = 0
        if keys[pygame.K_LEFT]:
            rotate -= 1
        if keys[pygame.K_RIGHT]:
            rotate += 1
        if keys[pygame.K_UP]:
            forward += 1
        if keys[pygame.K_DOWN]:
            forward -= 1
        if self.spin_count:
            spin = 1
            
        return (rotate, forward, spin)