from typing import AnyStr
import pygame
from constants import *
from math import floor
from utils.digits import digits

class ScoreBoard:
    def __init__(self):
        self.score = {"ally":0, "opponent":0}
        self.frame = pygame.image.load("resources/scoreboard.png")
        self.frame = pygame.transform.smoothscale_by(self.frame,SCOREBOARD_HEIGHT/self.frame.get_height())
        self.__draw_clock_colon__()
        self.time = 0
        self.clock = {"min": [0,0], "sec": [0,0], "ms": 0}
    
    def get_score(self):
        return self.score
    
    def update(self, character: AnyStr):
        curr_score = self.score.get(character)
        if curr_score == None:
            raise ScoreUpdateError("Cannot register multiple goals at once")
        self.score.update((character,curr_score + 1))
    
    def draw(self, screen, time):
        self.time += time
        self.__update_clock__()
        self.__draw_clock__()
        screen.blit(self.frame,((SCREEN_WIDTH-self.frame.get_width())/2,0))
        return screen
    
    def __update_clock__(self):
        ms = self.time%1000
        sec = floor(self.time/1000)%60
        min = floor(self.time/6e4)
        self.clock.update({"min": [floor(min/10),min%10], "sec": [floor(sec/10),sec%10], "ms": ms})
    
    def __draw_clock__(self):
        clock_entries = []
        for k in ["min","sec"]:
            [clock_entries.append(digits[i]) for i in self.clock.get(k)]
        for i, pos in enumerate(CLOCK_DIGIT_POSITIONS):
            self.frame.blit(clock_entries[i],pos)

    def __draw_clock_colon__(self):
        background = pygame.Surface((round(DIGIT_WIDTH/2),CLOCK_FRAME_HEIGHT))
        background.fill(BLACK)
        white_sqr = pygame.Surface((round(DIGIT_WIDTH/10),round(DIGIT_WIDTH/10)))
        white_sqr.fill(WHITE)
        center = background.get_rect().center
        background.blit(white_sqr,(center[0]-white_sqr.get_width()/2,center[1]-2*white_sqr.get_height()))
        background.blit(white_sqr,(center[0]-white_sqr.get_width()/2,center[1]+white_sqr.get_height()))
        self.frame.blit(background,(CLOCK_CENTER[0]-background.get_width()/2,CLOCK_CENTER[1]-background.get_height()/2))

    
class ScoreUpdateError(Exception):
    def __init__(self, value) -> None:
        self.value = value
    def __str__(self) -> str:
        return "Error: %s" % self.value