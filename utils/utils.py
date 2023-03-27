from typing import Tuple
import pygame


def get_screen_size() -> Tuple[int, int]:
    return pygame.display.get_surface().get_size()
