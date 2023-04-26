from pygame.sprite import Sprite, Group, spritecollide, collide_mask
import pygame
from game_elements.abstract_element import AbstractElement
from typing import List


class CollisionHandler:
    """
    stores a conversion scale from the Player unit system to 
    the actual rendering scale (which is still not the frame of reference of the screen),
    also keeps the mask, sprite and rect atributes valid for 
    appropriate collision management with the spritecollide and collide_mask functions
    """
    def __init__(self, scale):
        self.scale = scale

    def update_element_sprite(self, element: AbstractElement):
        """updates the collision relevant attributes of AbstractElement to the respective valid values"""
        element._sprite = pygame.transform.scale(element._surface, self.scale(element.size))
        element._sprite = pygame.transform.rotate(element._sprite, element._orientation)
        element.mask = pygame.mask.from_surface(element._sprite)
        element.rect = element._sprite.get_rect()
        element.rect.center = self.scale(element.get_pos())

    def check_collision(self, sprite: Sprite) -> bool:
        """this method is only supposed to be used by a Player, that's why the collision happens only when the group is of size 2,
        because this suffices to narrow down the group to the players attribute of the simulation"""
        for group in sprite.groups():
            if len(group) == 2:
                for element in CollisionHandler.group_collide(sprite, group):
                    return True
        return False

    @staticmethod
    def group_collide(sprite: Sprite, group: Group) -> List[Sprite]:
        """simply exposes and converts the return value of the spritecollide function to its desired form, i.e., a list of Sprites or an empty list"""
        return [element for element in spritecollide(sprite, group, False, collided=CollisionHandler.collision_handler)]

    @staticmethod
    def collision_handler(sprite1: Sprite, sprite2: Sprite):
        """only exists to exclude detection of collision of a sprite with itself"""
        collision_point = collide_mask(sprite1, sprite2)
        return collision_point != None and sprite1 != sprite2