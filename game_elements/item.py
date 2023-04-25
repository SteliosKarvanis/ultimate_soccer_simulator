import pygame
from pygame.sprite import Sprite, Group
from game_elements.player import Player
from enum import Enum
from game_elements.effects import *

ITEM_SIZE = (0.055, 0.055)

class ItemState(Enum):
    WAITING = 0,
    IN_USE = 1

class Item (Sprite):
    def __init__(self, pos, birth_time) -> None:
        super().__init__()
        self.image = pygame.image.load("resources/item.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.size = ITEM_SIZE
        self.pos = (pos[0], pos[1])
        self.rect = self.image.get_rect(center=self.pos)
        self.lifetime = 0
        self.__set_lifetime__()
        self.effect_duration = 0
        self.__set_duration__()
        self.state = ItemState.WAITING
        self.effect = None
        self.current_user = None
        self.existence_time = birth_time
        self.use_time = None

    # should define a lifetime in miliseconds for each concrete item
    def __set_lifetime__(self):
        raise NotImplementedError(
            "This method is abstract and must be implemented in derived classes"
        )

    # should define a duration in miliseconds for each concrete item
    def __set_duration__(self):
        raise NotImplementedError(
            "This method is abstract and must be implemented in derived classes"
        )
    
    # should define the concrete effect once the item is touched by a player
    def __create_effect__(self, player: Player):
        raise NotImplementedError(
            "This method is abstract and must be implemented in derived classes"
        )
    
    def update(self, time: int, players: Group) -> Player|None:
        match self.state:
            case ItemState.IN_USE:
                self.effect_duration -= (time - self.use_time)
                self.use_time = time
                if self.effect_duration <= 0:
                    for group in self.groups():
                        group.remove(self)
                    self.effect.restore(self.current_user)
                return None
                
            case ItemState.WAITING:
                self.lifetime -= (time - self.existence_time)
                self.existence_time = time
                player = self.check_collision(players)
                if self.lifetime <= 0:
                    for group in self.groups():
                        group.remove(self)
                if player != None:
                    self.lifetime = 0
                    self.state = ItemState.IN_USE
                    self.current_user = player
                    self.__create_effect__(player)
                    self.use_time = time
                return player

    def check_collision(self, players: Group)-> Player|None:
        players = pygame.sprite.spritecollide(self, players, False, collided=Item.collided)
        return players[0] if len(players) != 0 else None
   
    @staticmethod
    def collided(item: Sprite, player: Player)->bool:
        collision_point = pygame.sprite.collide_mask(item, player)
        return collision_point != None


class Accelerator(Item):
    def __set_lifetime__(self):
        self.lifetime = 10e3

    def __set_duration__(self):
        self.effect_duration = 5e3
    
    def __create_effect__(self, player: Player):
        self.effect = IncreaseSpeed(player)

class Mushroom(Item):
    def __set_lifetime__(self):
        self.lifetime = 10e3

    def __set_duration__(self):
        self.effect_duration = 3e3
    
    def __create_effect__(self, player: Player):
        self.effect = IncreaseSize(player)

item_type_list = [Mushroom, Accelerator]