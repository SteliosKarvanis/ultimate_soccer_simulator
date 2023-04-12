from math import pi


def wrap_to_pi(angle: float) -> float:
    angle = angle % (2 * pi)
    if angle > pi:
        angle = angle - 2 * pi
    return angle
