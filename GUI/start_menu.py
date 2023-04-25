import pygame
from utils.configs import Configuration
from pygame.colordict import THECOLORS as colors

class Start_Menu():
    def __init__(self) -> None:
        self.configs=Configuration()
        self.background_color=(0,255,0)
        self.text1='Welcome to ultimate soccer simulator!'
        self.text2='Press any button on keyboard to start'
        self.text3='To move foward/backward, use the up/down arrow keys'
        self.text4='To rotate to right/left, use the right/left arrow keys'
        self.text_color=(255,255,255)
        

