from typing import Tuple
from math import radians, cos, sin, degrees
import pygame
from game_elements.abstract_element import AbstractElement
from game_elements.field import LEFT_FRONT_GOAL_X, FIELD_LENGTH_Y, TOP_GOAL_Y
from game_elements.player import Player
from utils.configs import SAMPLE_TIME
from utils.utils import (
    polar_to_cartesian_vector,
    cartesian_to_polar_vector,
    get_state_from_referential,
    get_state_in_referential,
    translate_vector,
)


BALL_DIAMETER = 0.0427
FRICTION = 4.0
BALL_RADIUS = BALL_DIAMETER / 2
TOLERANCE = BALL_RADIUS / 2
BALL_SIZE = (BALL_DIAMETER, BALL_DIAMETER)


class Ball(AbstractElement):
    def __init__(self, initial_pos: Tuple = (0, 0)):
        super().__init__(initial_pos=initial_pos, vel=0, size=BALL_SIZE)
        self._radius = BALL_RADIUS
        self._surface = pygame.image.load("resources/ball.png")

    def reset_state(self):
        self._vel = 0
        self._orientation = 0
        self._x, self._y = 0, 0
        
    def update(self) -> str:
        collision_side = self.get_bumper_state()
        if collision_side == "up" or collision_side == "down":
            self._orientation = (360 - self._orientation) % 360
        elif collision_side == "right" or collision_side == "left":
            self._orientation = (180 - self._orientation) % 360
        self._x, self._y = translate_vector(
            self.get_pos(), polar_to_cartesian_vector(self._vel * SAMPLE_TIME, radians(self._orientation))
        )
        self.update_velocity()
        goal_state = self.get_goal_state()
        if goal_state != "None":
            self.reset_state()
        return goal_state

    def update_velocity(self) -> float:
        new_vel = self._vel - FRICTION * SAMPLE_TIME
        return max(new_vel, 0)

    def get_bumper_state(self) -> str:
        if self._y + BALL_RADIUS >= FIELD_LENGTH_Y / 2:
            return "up"
        elif self._y - BALL_RADIUS <= -FIELD_LENGTH_Y / 2:
            return "down"
        elif self._y + BALL_RADIUS >= TOP_GOAL_Y or self._y - BALL_RADIUS <= -TOP_GOAL_Y:
            if self._x - BALL_RADIUS <= LEFT_FRONT_GOAL_X:
                return "left"
            elif self._x + BALL_RADIUS >= -LEFT_FRONT_GOAL_X:
                return "right"
            else:
                return "None"
        else:
            return "None"

    def get_goal_state(self) -> str:
        if self._x >= -LEFT_FRONT_GOAL_X:
            # player made a goal
            return "ally"
        elif self._x <= LEFT_FRONT_GOAL_X:
            # adversary made a goal
            return "opponent"
        else:
            return "None"

    def collision_management(self, element: Player) -> bool:
        referential_state = element.get_state()
        side_x, side_y = element.size
        collided = False
        # Changing to the referential of the element
        x, y, orientation, v = get_state_in_referential(state=self.get_state(), referential_state=referential_state)
        v_x, v_y = polar_to_cartesian_vector(v, radians(orientation))
        # Check if has collision
        if abs(x) < BALL_RADIUS + side_x / 2 and abs(y) < BALL_RADIUS + side_x / 2:
            collided = True
            # Check which side collided
            y_top = side_y / 2 + BALL_RADIUS
            y_bottom = -y_top
            x_right = side_x / 2 + BALL_RADIUS
            x_left = -x_right
            # For each vertex, check it is above the line of movement of the ball, for example tr == True, check if the top right vertex is above the movement line of the ball
            a = -sin(radians(orientation))
            b = cos(radians(orientation))
            tr = (a * (x_right - x) + b * (y_top - y)) > 0
            br = (a * (x_right - x) + b * (y_bottom - y)) > 0
            tl = (a * (x_left - x) + b * (y_top - y)) > 0
            bl = (a * (x_left - x) + b * (y_bottom - y)) > 0
            # right side colision
            if ((tr and not br) or (br and not tr)) and (orientation > 90 and orientation < 270):
                x = BALL_RADIUS + side_x / 2 + TOLERANCE
                v, orientation_rad = cartesian_to_polar_vector(-0.5 * v_x, v_y)
                orientation = degrees(orientation_rad)
            # left side colision
            elif ((tl and not bl) or (bl and not tl)) and (orientation < 90 or orientation > 270):
                x = -BALL_RADIUS - side_x / 2 - TOLERANCE
                v, orientation_rad = cartesian_to_polar_vector(-0.5 * v_x, v_y)
                orientation = degrees(orientation_rad)
            # top side colision
            if ((tr and not tl) or (tl and not tr)) and orientation > 180:
                y = BALL_RADIUS + side_y / 2 + TOLERANCE
                v, orientation_rad = cartesian_to_polar_vector(v_x, -0.5 * v_y)
                orientation = degrees(orientation_rad)
            # bottom side colision
            elif ((bl and not br) or (br and not bl)) and orientation < 180:
                y = -BALL_RADIUS - side_y / 2 - TOLERANCE
                v, orientation_rad = cartesian_to_polar_vector(v_x, -0.5 * v_y)
                orientation = degrees(orientation_rad)
        # TODO: check if has collision in spinning or only wit angular rotation
        # Back to the global referential
        if collided:
            self._x, self._y, self._orientation, self._vel = get_state_from_referential(
                state=(x, y, orientation, v), referential_state=referential_state
            )
        return collided
