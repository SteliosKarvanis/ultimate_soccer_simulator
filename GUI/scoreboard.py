from typing import Dict, List
import pygame
from pygame import Surface
from math import floor
from utils.digits import digits, DIGIT_WIDTH, CLOCK_FRAME_HEIGHT

CLOCK_POS = (93, 61)
CLOCK_DIG_POS = [(CLOCK_POS[0] + k * DIGIT_WIDTH, CLOCK_POS[1]) for k in [0, 1, 2.5, 3.5]]
ALLY_SCORE_POS = (32, 51)
SCORES_DIG_POS = [(ALLY_SCORE_POS[0] + k * DIGIT_WIDTH, ALLY_SCORE_POS[1]) for k in [0, 1, 10.5, 11.5]]


class ScoreBoard:
    def __init__(self, frame_height: float):
        self.frame = pygame.image.load("resources/scoreboard.png")
        self.score, self.score_digits = self.__create_scores__()
        self.__update_assets__(frame_height)
        self.time = 0  # tracks time in ms
        # keeps the appropriate representation for the scoreboard
        self.clock, self.clock_digits = self.__create_clock__()

    def get_score(self):
        return self.score

    def update(self, character: str, frame_height: float):
        curr_score = self.score.get(character)
        if curr_score == None:
            raise ScoreUpdateError("Cannot register multiple goals at once")
        if curr_score >= 99:
            raise ScoreUpdateError("Scoreboard cannot count with 3 digits")
        self.score.update([(character, curr_score + 1)])
        self.__update_assets__(frame_height)

    def draw(self, screen: Surface, time: int):
        self.time += time
        self.__update_clock__()
        screen.blit(self.frame, ((screen.get_width() - self.frame.get_width()) / 2, 0))
        return screen

    def __update_assets__(self, frame_height: float):
        pygame.transform.scale_by(self.frame, frame_height / self.frame.get_height())
        self.__update_scores__()

    def __create_scores__(self):
        surfs = [self.frame.subsurface(SCORES_DIG_POS[2 * k], (2 * DIGIT_WIDTH, CLOCK_FRAME_HEIGHT)) for k in range(2)]
        digs = [surfs[i].subsurface((k * DIGIT_WIDTH, 0), (DIGIT_WIDTH, CLOCK_FRAME_HEIGHT)) for i in range(2) for k in range(2)]
        return {"ally": 00, "opponent": 00}, {
            "ally": [digs[0], digs[1]],
            "opponent": [digs[2], digs[3]],
        }

    def __update_scores__(self):
        for k in ["ally", "opponent"]:
            n = self.score.get(k)
            self.score_digits.get(k)[0].blit(digits[floor(n / 10) % 10], (0, 0))
            self.score_digits.get(k)[1].blit(digits[n % 10], (0, 0))

    # don't even ask
    def __create_clock__(self) -> List[Dict]:
        surfs = [self.frame.subsurface(CLOCK_DIG_POS[2 * k], (2 * DIGIT_WIDTH, CLOCK_FRAME_HEIGHT)) for k in range(2)]
        digs = [surfs[i].subsurface((k * DIGIT_WIDTH, 0), (DIGIT_WIDTH, CLOCK_FRAME_HEIGHT)) for i in range(2) for k in range(2)]
        return {"min": [0, 0], "sec": [0, 0]}, {
            "min": [digs[0], digs[1]],
            "sec": [digs[2], digs[3]],
        }

    def __update_clock__(self):
        sec = floor(self.time / 1000) % 60
        min = floor(self.time / 6e4)
        dig_nums = [floor(min / 10), min % 10, floor(sec / 10), sec % 10]
        digs = [digits[d] for d in dig_nums]
        for i, k in enumerate(["min", "sec"]):
            [self.clock_digits.get(k)[j].blit(digs[j + 2 * i], (0, 0)) for j in range(2)]
            self.clock.update({k: dig_nums[2 * i : 2 * i + 2]})


class ScoreUpdateError(Exception):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return "Error: %s" % self.value
