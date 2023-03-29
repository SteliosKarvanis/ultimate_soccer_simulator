from typing import Tuple
import pygame
from math import pi


def degree_to_rad(angle: float) -> float:
    return angle * pi / 180


def rad_to_degree(angle: float) -> float:
    return angle * 180 / pi


def wrap_to_pi(angle: float) -> float:
    angle = angle % (2 * pi)
    if angle > pi:
        angle = angle - 2 * pi
    return angle
