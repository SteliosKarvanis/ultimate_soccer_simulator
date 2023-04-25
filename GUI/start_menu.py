import pygame
from utils.configs import Configuration

class Start_Menu():
    def __init__(self) -> None:
        self.configs=Configuration()
        self.screen=pygame.display.set_mode(self.configs.screen_res)
        self.width = self.screen.get_width()
        self.height=self.screen.get_height()
        self.text1='welcome to ultimate soccer simulator!'
        self.text2='press any buttom on keyboard to start'
        self.text3='to move foward/backward, use up/down arrow keys'
        self.text4='to rotate to right/left, use right/left arrow keys'
        self.text_color=(255,255,255)
        self.background_color=(0,0,0)

