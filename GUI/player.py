import pygame
from typing import Tuple
from constants import *
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, initial_pos: Tuple = (SCREEN_HEIGHT/2, SCREEN_WIDTH/2), orientation: float = 0):
        super(Player, self).__init__()
        self.surface = pygame.Surface(PLAYER_SIZE)
        self.surface.set_colorkey(BACKGROUND_COLOR)
        self.surface.fill(WHITE)
        self._x, self._y = initial_pos
        self._orientation = orientation
        self.spin_count = 0


    def get_pos(self) -> Tuple:
        return self._x, self._y
    

    def get_orientation(self) -> float:
        return self._orientation
    

    def actions(self, keys: pygame.key.ScancodeWrapper):
        linear_move = 0
        angular_move = 0
        if keys[pygame.K_SPACE] or self.spin_count:
            self.spin_count += 1
            self._orientation = (self._orientation + SPIN_SPEED) % 360
            if self.spin_count >= SPIN_COUNTDOWN:
                self.spin_count = 0
        else:
            if keys[pygame.K_LEFT]:
                angular_move -= PLAYER_ANGULAR_SPEED
            if keys[pygame.K_RIGHT]:
                angular_move += PLAYER_ANGULAR_SPEED
            if keys[pygame.K_UP]:
                linear_move += PLAYER_LINEAR_SPEED
            if keys[pygame.K_DOWN]:
                linear_move -= PLAYER_LINEAR_SPEED
            self._orientation = (self._orientation + angular_move) % 360
            self._x = self._x + math.sin(self._orientation*math.pi/180)*linear_move
            self._y = self._y + math.cos(self._orientation*math.pi/180)*linear_move
    
    def draw_player(self):
        surface = pygame.transform.rotate(self.surface, self._orientation)
        rect = surface.get_rect()
        rect.center = self.get_pos()
        return surface, rect