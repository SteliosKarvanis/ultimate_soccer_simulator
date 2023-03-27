from pygame.math import Vector2


class WorldState:
    def __init__(
        self,
        player_pos: Vector2,
        player_orientation: float,
        opponent_pos: Vector2,
        opponent_orientation: float,
        ball_pos: Vector2,
    ) -> None:
        self.player_pos = player_pos
        self.player_orientation = player_orientation
        self.opponent_pos = opponent_pos
        self.opponent_orientation = opponent_orientation
        self.ball_pos = ball_pos
