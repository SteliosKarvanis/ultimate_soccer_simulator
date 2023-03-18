from typing import AnyStr
import pygame
from constants import *

class ScoreBoard:
    def __init__(self):
        self.score = {"ally":0, "opponent":0}
        self.frame = pygame.image.load("resources/scoreboard.png")
        self.frame = pygame.transform.smoothscale_by(self.frame,SCOREBOARD_HEIGHT/self.frame.get_height())
    def get_score(self):
        return self.score
    def update(self, character: AnyStr):
        curr_score = self.score.get(character)
        if curr_score == None:
            raise ScoreUpdateError("Cannot register multiple goals at once")
        self.score.update((character,curr_score + 1))
    def draw(self, screen):
        screen.blit(self.frame,((SCREEN_WIDTH-self.frame.get_width())/2,0))
        return screen
    
class ScoreUpdateError(Exception):
    def __init__(self, value) -> None:
        self.value = value
    def __str__(self) -> str:
        return "Error: %s" % self.value