from enum import Enum


class CollisionType(Enum):
    NONE = 0
    WITH_SCENERY = 1
    OF_PLAYERS = 2
    BALL_PLAYER = 3
    ON_LEFT_GOAL = 4
    ON_RIGHT_GOAL = 5
