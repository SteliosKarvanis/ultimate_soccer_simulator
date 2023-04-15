from typing import Tuple


class WorldState:
    def __init__(self, player_state: Tuple, opponent_state: Tuple, ball_state: Tuple) -> None:
        self.player_state = player_state
        self.opponent_state = opponent_state
        self.ball_state = ball_state
