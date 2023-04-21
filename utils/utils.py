from typing import Sequence, Tuple
from math import pi, cos, sin, acos, sqrt, degrees, radians


def reflect_vector_vertically(point: Tuple[float, float]):
    return point[0], -point[1]


def reflect_vector_horizontally(point: Tuple[float, float]):
    return -point[0], point[1]


def opposite_vector(point: Tuple[float, float]):
    return -point[0], -point[1]


def subtract_vector(v1: Tuple[float, float], v2: Tuple[float, float]) -> Tuple[float, float]:
    return v1[0] - v2[0], v1[1] - v2[1]


def rotate_vector(vector: Sequence, angle_rad: float) -> Tuple[float, float]:
    x0 = vector[0]
    y0 = vector[1]
    x = x0 * cos(angle_rad) + y0 * sin(angle_rad)
    y = -x0 * sin(angle_rad) + y0 * cos(angle_rad)
    return x, y


def cartesian_to_polar_vector(x: float, y: float) -> Tuple[float, float]:
    magnitude = sqrt(x**2 + y**2)
    if magnitude != 0:
        theta_rad = acos(x / magnitude)
        if y < 0:
            theta_rad = 2 * pi - theta_rad
    else:
        theta_rad = 0
    return magnitude, theta_rad


def get_magnitude_from_vector(x: float, y: float) -> float:
    return sqrt(x**2 + y**2)


def polar_to_cartesian_vector(magnitude: float, angle_rad: float) -> Tuple[float, float]:
    return magnitude * cos(angle_rad), magnitude * sin(angle_rad)


def translate_vector(vector: Sequence, move: Sequence) -> Tuple[float, float]:
    return vector[0] + move[0], vector[1] + move[1]


def get_state_in_referential(state: Tuple, referential_state: Tuple) -> Tuple[float, float]:
    # Referential pose in world
    rf_x, rf_y, rf_theta_deg, rf_v = referential_state
    rf_theta_rad = radians(rf_theta_deg)
    v_rf_x, v_rf_y = polar_to_cartesian_vector(rf_v, rf_theta_rad)

    # Pose on global referential
    x0, y0, theta0_deg, v0 = state
    theta0_rad = radians(theta0_deg)
    v0_x, v0_y = polar_to_cartesian_vector(v0, theta0_rad)

    # Make relative positions (translation and rotation)
    x0, y0 = translate_vector((x0, y0), (-rf_x, -rf_y))
    x, y = rotate_vector((x0, y0), rf_theta_rad)

    # Make relative velocities (translation and rotation)
    v0_x, v0_y = translate_vector((v0_x, v0_y), (-v_rf_x, -v_rf_y))
    v_x, v_y = rotate_vector((v0_x, v0_y), rf_theta_rad)

    v, theta_rad = cartesian_to_polar_vector(v_x, v_y)
    theta_deg = degrees(theta_rad)
    new_state = (x, y, theta_deg, v)
    return new_state


def get_state_from_referential(state: Tuple, referential_state: Tuple) -> Tuple:
    # Referential pose in world
    rf_x, rf_y, rf_theta_deg, rf_v = referential_state
    rf_theta_rad = radians(rf_theta_deg)
    rf_v_x, rf_v_y = polar_to_cartesian_vector(rf_v, rf_theta_rad)

    # Pose on global referential
    x0, y0, theta0_deg, v0 = state
    theta0_rad = radians(theta0_deg)
    v0_x, v0_y = polar_to_cartesian_vector(v0, theta0_rad)

    # Make relative positions (translation and rotation)
    x, y = rotate_vector((x0, y0), -rf_theta_rad)
    x, y = translate_vector((x, y), (rf_x, rf_y))

    # Make relative velocities (translation and rotation)
    v_x, v_y = rotate_vector((v0_x, v0_y), -rf_theta_rad)
    v_x, v_y = translate_vector((v_x, v_y), (rf_v_x, rf_v_y))

    v, theta_rad = cartesian_to_polar_vector(v_x, v_y)
    theta_deg = degrees(theta_rad)
    new_state = (x, y, theta_deg, v)
    return new_state
