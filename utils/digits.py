from typing import Sequence
from pygame import Surface, transform
from pygame.colordict import THECOLORS as colors

DIGIT_WIDTH = 15
CLOCK_FRAME_HEIGHT = 35

binaries = [
    [1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 0, 1],
    [0, 1, 1, 0, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
]

seg_length = round(DIGIT_WIDTH * 0.8)
seg_width = round(seg_length / 8)
horiz_rect = Surface((seg_length, seg_width))
horiz_rect.fill(colors.get("white"))
vert_rect = Surface((seg_width, seg_length))
vert_rect.fill(colors.get("white"))

segments = [
    [(DIGIT_WIDTH - seg_width, seg_width), vert_rect],
    [(DIGIT_WIDTH - seg_width, CLOCK_FRAME_HEIGHT - seg_width - seg_length), vert_rect],
    [(seg_width, CLOCK_FRAME_HEIGHT - seg_width), horiz_rect],
    [(0, CLOCK_FRAME_HEIGHT - seg_width - seg_length), vert_rect],
    [(0, seg_width), vert_rect],
    [(seg_width, 0), horiz_rect],
    [(seg_width, round((CLOCK_FRAME_HEIGHT - seg_width) / 2)), horiz_rect],
]


def get_segments(n: int) -> Sequence[bool]:
    assert n % 10 == n
    return binaries[n]


def draw_digit(n: int) -> Surface:
    digit = Surface((DIGIT_WIDTH, CLOCK_FRAME_HEIGHT))
    digit.fill(colors.get("black"))
    for i, draw in enumerate(get_segments(n)):
        if draw:
            pos = segments[i][0]
            segment = segments[i][1]
            digit.blit(segment, pos)
    frame = Surface((DIGIT_WIDTH, CLOCK_FRAME_HEIGHT))
    frame.fill(colors.get("black"))
    ratio = 0.8
    digit = transform.smoothscale_by(digit, ratio)
    frame.blit(digit, ((1 - ratio) / 2 * DIGIT_WIDTH, (1 - ratio) / 2 * CLOCK_FRAME_HEIGHT))
    return frame


digits = [draw_digit(n) for n in range(10)]
