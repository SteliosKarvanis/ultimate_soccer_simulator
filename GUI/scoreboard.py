from typing import Tuple

class ScoreBoard:
    def __init__(self):
        self.score = (0, 0)

    def update(self, score: Tuple):
        self.score = score

    def draw(self):
        pass