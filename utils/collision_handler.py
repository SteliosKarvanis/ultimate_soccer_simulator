from pygame.sprite import Sprite, Group, spritecollide, collide_mask
import pygame
from game_elements.abstract_element import AbstractElement
from typing import List


class CollisionHandler:
    def __init__(self, scale):
        self.scale = scale

    def update_element_sprite(self, element: AbstractElement):
        element._sprite = pygame.transform.scale(element._surface, self.scale(element.size))
        element._sprite = pygame.transform.rotate(element._sprite, element._orientation)
        element.mask = pygame.mask.from_surface(element._sprite)
        element.rect = element._sprite.get_rect()
        element.rect.center = self.scale(element.get_pos())

    def check_collision(self, sprite: Sprite) -> bool:
        for group in sprite.groups():
            if len(group) == 2:
                for element in CollisionHandler.group_collide(sprite, group):
                    return True
        return False

    @staticmethod
    def group_collide(sprite: Sprite, group: Group) -> List[Sprite]:
        return [element for element in spritecollide(sprite, group, False, collided=CollisionHandler.collision_handler)]

    @staticmethod
    def collision_handler(sprite1: Sprite, sprite2: Sprite):
        collision_point = collide_mask(sprite1, sprite2)
        return collision_point != None and sprite1 != sprite2