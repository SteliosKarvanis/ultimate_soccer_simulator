from typing import Tuple
from pygame import Surface


class Point(Tuple[float, float]):
    def __init__(self) -> None:
        super().__init__()


class GameElement:
    def __init__(self) -> None:
        self._x = 0
        self._y = 0
        self._orientation = 0

    def get_pos(self) -> Point:
        return self._x, self._y

    def get_orientation(self) -> float:
        return self._orientation

    def get_pose(self) -> Tuple[float, float, float]:
        return self._orientation, self._x, self._y

    def get_sprite(self) -> Surface:
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")
