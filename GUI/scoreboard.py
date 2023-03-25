from typing import AnyStr,Dict
import pygame
from pygame import Surface
from constants import *
from math import floor
from utils.digits import digits

class ScoreBoard:
    def __init__(self, frame_height: int):
        self.score = {"ally": 0, "opponent": 0}
        self.frame = pygame.image.load("resources/scoreboard.png")
        self.frame = pygame.transform.smoothscale_by(self.frame,frame_height/self.frame.get_height())
        self.time = 0 # tracks time in ms
        # keeps the appropriate representation for the scoreboard
        self.clock = {"min": [0,0], "sec": [0,0], "ms": 0}
        self.__draw_scores__()
    def get_score(self):
        return self.score
    
    def update(self, character: AnyStr):
        curr_score = self.score.get(character)
        if curr_score == None:
            raise ScoreUpdateError("Cannot register multiple goals at once")
        if curr_score >= 99:
            raise ScoreUpdateError("Scoreboard cannot count with 3 digits")
        self.score.update((character,curr_score + 1))
        self.__draw_scores__()
    
    def draw(self, screen: Surface, time):
        self.time += time
        self.__update_clock__()
        self.__draw_clock__()
        screen.blit(self.frame,((screen.get_width()-self.frame.get_width())/2,0))
        return screen
    

    def __update_clock__(self):
        ms = self.time%1000
        sec = floor(self.time/1000)%60
        min = floor(self.time/6e4)
        self.clock.update({"min": [floor(min/10),min%10], "sec": [floor(sec/10),sec%10], "ms": ms})

    def __draw_scores__(self):
        pos = self.__get_scores_digits_positions()
        for k in ["ally", "opponent"]:
            n = self.score.get(k)
            self.frame.blit(digits[floor(n/10)%10],pos.get(k)[0])
            self.frame.blit(digits[n%10],pos.get(k)[1])
    
    def __get_scores_digits_positions(self) -> Dict:
        ally_digits_pos = [[0,0],[0,0]]
        opponent_digits_pos = [[0,0],[0,0]]
        ally_digits_pos[0][0] = -digits[0].get_width() + SCORES_CENTERS.get("ally")[0]
        ally_digits_pos[0][1] = -digits[0].get_height()/2 + SCORES_CENTERS.get("ally")[1]
        ally_digits_pos[1][1] = ally_digits_pos[0][1]
        ally_digits_pos[1][0] = SCORES_CENTERS.get("ally")[0]
        opponent_digits_pos[0][0] = -digits[0].get_width() + SCORES_CENTERS.get("opponent")[0]
        opponent_digits_pos[0][1] = -digits[0].get_height()/2 + SCORES_CENTERS.get("opponent")[1]
        opponent_digits_pos[1][1] = opponent_digits_pos[0][1]
        opponent_digits_pos[1][0] = SCORES_CENTERS.get("opponent")[0]
        return {"ally": ally_digits_pos, "opponent": opponent_digits_pos}


    # Draws digits of current game time to the clock in the scoreboard
    def __draw_clock__(self):
        clock_entries = []
        for k in ["min","sec"]:
            [clock_entries.append(digits[i]) for i in self.clock.get(k)]
        for i, pos in enumerate(CLOCK_DIGIT_POSITIONS):
            self.frame.blit(clock_entries[i],pos)

    
class ScoreUpdateError(Exception):
    def __init__(self, value) -> None:
        self.value = value
    def __str__(self) -> str:
        return "Error: %s" % self.value