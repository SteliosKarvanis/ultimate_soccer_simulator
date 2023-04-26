import pygame
from pygame.sprite import Sprite, Group
from pygame.math import Vector2
from game_elements.player import Player
from enum import Enum
from game_elements.effects import *
from pygame.colordict import THECOLORS as colors

ITEM_SIZE = (0.06, 0.06)

class Message:
    def __init__(self, sprite: pygame.Surface, pos: Vector2) -> None:
        self.msg = sprite
        self.pos = pos
        self.lifetime = 1e3
        self.birth_time = 0
    
class ItemState(Enum):
    WAITING = 0,
    IN_USE = 1

class Item (Sprite):
    def __init__(self, pos, birth_time) -> None:
        super().__init__()
        self.name = ""
        self.font = pygame.font.SysFont('Times New Roman', 35, bold=True)
        self.text_color = colors.get("white")
        self.msg = self.font.render(self.name, True, self.text_color)
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

    def check_collision(self, players: Group) -> Player|None:
        players = pygame.sprite.spritecollide(self, players, False, collided=Item.collided)
        return players[0] if len(players) != 0 else None
        
    def create_message(self, player: Player) -> Message:
        return Message(self.msg, player.get_pos())
    
    @staticmethod
    def collided(item: Sprite, player: Player) -> bool:
        collision_point = pygame.sprite.collide_mask(item, player)
        return collision_point != None


class Accelerator(Item):
    def __init__(self, pos, birth_time) -> None:
        super().__init__(pos, birth_time)
        self.name = "Speed!"
        self.msg = self.font.render(self.name, False, self.text_color)

    def __set_lifetime__(self):
        self.lifetime = 10e3

    def __set_duration__(self):
        self.effect_duration = 5e3
    
    def __create_effect__(self, player: Player):
        self.effect = IncreaseSpeed(player)

class Mushroom(Item):
    def __init__(self, pos, birth_time) -> None:
        super().__init__(pos, birth_time)
        self.name = "Grow!"
        self.text_color = colors.get("orange")
        self.msg = self.font.render(self.name, False, self.text_color)

    def __set_lifetime__(self):
        self.lifetime = 10e3

    def __set_duration__(self):
        self.effect_duration = 4e3
    
    def __create_effect__(self, player: Player):
        self.effect = IncreaseSize(player)

item_type_list = [Mushroom, Accelerator]