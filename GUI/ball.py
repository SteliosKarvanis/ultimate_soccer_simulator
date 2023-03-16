import pygame
from constants import *


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        self.pos = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.vel = 0
        self.orientation = 0

    def update(self, action):
        pass

    
    def draw(self, screen):
        pygame.draw.circle(screen, RED, self.pos, BALL_RADIUS)
        return screen