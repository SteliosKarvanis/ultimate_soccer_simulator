from typing import Tuple
from math import pi, cos, sin, acos, sqrt


def rotate_vector(x0: float, y0: float, angle_rad: float) -> Tuple[float, float]:
    x = x0 * cos(angle_rad) + y0 * sin(angle_rad)
    y = -x0 * sin(angle_rad) + y0 * cos(angle_rad)
    return x, y


def cartesian_to_polar_vector(v_x: float, v_y: float) -> Tuple[float, float]:
    v = sqrt(v_x**2 + v_y**2)
    if v != 0:
        theta_rad = acos(v_x / v)
        if v_y < 0:
            theta_rad = 2 * pi - theta_rad
    else:
        theta_rad = 0
    return v, theta_rad


def polar_to_cartesian_vector(v: float, angle_rad: float) -> Tuple[float, float]:
    return v * cos(angle_rad), v * sin(angle_rad)


def translate_vector(x0: float, y0: float, delta_x: float, delta_y: float) -> Tuple[float, float]:
    return x0 + delta_x, y0 + delta_y
