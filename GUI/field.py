FIELD_LENGTH_X = 1200
FIELD_LENGTH_Y = 640
GOAL_LENGTH_X = 80
GOAL_LENGTH_Y = 200

TOP_GOAL_Y = GOAL_LENGTH_Y / 2
TOP_FIELD_Y = FIELD_LENGTH_Y / 2
LEFT_GOAL_X = -FIELD_LENGTH_X / 2
LEFT_FRONT_GOAL_X = LEFT_GOAL_X + GOAL_LENGTH_X

FIELD_POINTS = [
    (LEFT_GOAL_X, -TOP_GOAL_Y),
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
