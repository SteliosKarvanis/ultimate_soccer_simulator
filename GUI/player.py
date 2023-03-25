import pygame
from typing import Tuple
from constants import *
import math
from utils.agent_actions import Action

class Player(pygame.sprite.Sprite):
    def __init__(self, initial_pos: Tuple = (SCREEN_HEIGHT/2, SCREEN_WIDTH/2), orientation: float = 0, color = WHITE):
        super().__init__()
        self.surface = pygame.Surface(PLAYER_SIZE)
        self.surface.set_colorkey(BACKGROUND_COLOR)
        self.surface.fill(color)
        self._x, self._y = initial_pos
        self._orientation = orientation


    def get_pos(self) -> Tuple:
        return self._x, self._y
    

    def get_orientation(self) -> float:
        return self._orientation
    
    def get_pose(self) -> Tuple:
        return self._x, self._y, self._orientation
    

    def update(self, action: Action):
        if action.spin:
            self._orientation = (self._orientation - action.spin*PLAYER_SPIN_SPEED*action.spin) % 360
        else:
            self._orientation = (self._orientation - action.rotate*PLAYER_ANGULAR_SPEED) % 360
            self._x = self._x + math.sin(self._orientation * math.pi/180)*PLAYER_LINEAR_SPEED*action.forward
            self._y = self._y + math.cos(self._orientation*math.pi/180)*PLAYER_LINEAR_SPEED*action.forward


    def draw(self, screen):
        surface = pygame.transform.rotate(self.surface, self._orientation)
        rect = surface.get_rect()
        rect.center = self.get_pos()
        screen.blit(source=surface, dest=rect)
        return screen