from typing import Tuple
import operator
import pygame

FIELD_LINE_THICKNESS = 10
LEFT_GOAL_X = -600
GOAL_LENGTH_X = 80
TOP_GOAL_Y = 100
TOP_FIELD_Y = 300
LEFT_FRONT_GOAL_X = LEFT_GOAL_X + GOAL_LENGTH_X

FIELD_POINTS = [(LEFT_GOAL_X, -TOP_GOAL_Y),
                (LEFT_GOAL_X, TOP_GOAL_Y), 
                (LEFT_FRONT_GOAL_X, TOP_GOAL_Y), 
                (LEFT_FRONT_GOAL_X, TOP_FIELD_Y), 
                (-LEFT_FRONT_GOAL_X, TOP_FIELD_Y),
                (-LEFT_FRONT_GOAL_X, TOP_GOAL_Y),
                (-LEFT_GOAL_X, TOP_GOAL_Y),
                (-LEFT_GOAL_X, -TOP_GOAL_Y),
                (-LEFT_FRONT_GOAL_X, -TOP_GOAL_Y),
                (-LEFT_FRONT_GOAL_X, -TOP_FIELD_Y),
                (LEFT_FRONT_GOAL_X, -TOP_FIELD_Y),
                (LEFT_FRONT_GOAL_X, -TOP_GOAL_Y),
                ]

def draw_field(screen, center_pos: Tuple[int]):
    field_points = [tuple(map(operator.add, x, center_pos)) for x in FIELD_POINTS]
    pygame.draw.lines(surface=screen, color=pygame.Color("white"), closed=True, points=field_points, width=FIELD_LINE_THICKNESS)
    return screen
