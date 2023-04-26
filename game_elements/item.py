import pygame
from pygame.sprite import Sprite, Group
from pygame.math import Vector2
from game_elements.player import Player
from enum import Enum
from game_elements.effects import *
from pygame.colordict import THECOLORS as colors

ITEM_SIZE = (0.06, 0.06)

class Message:
    """stores a sprite to be drawn with the message of an item and tracks its permanence in the screen"""
    def __init__(self, sprite: pygame.Surface, pos: Vector2) -> None:
        self.msg = sprite
        self.pos = pos
        self.lifetime = 1e3 # duration
        self.birth_time = 0 # creation time
    
    def create(self, time):
        """registers creation time"""
        self.birth_time = time

class ItemState(Enum):
    """represents the two possible states of an item (unused and in use)"""
    WAITING = 0,
    IN_USE = 1

class Item (Sprite):
    def __init__(self, pos, birth_time) -> None:
        super().__init__()
        self.name = "" # message in str form
        self.font = pygame.font.SysFont('Times New Roman', 35, bold=True)
        self.text_color = colors.get("white")
        self.msg = self.font.render(self.name, True, self.text_color)
        self.image = pygame.image.load("resources/item.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.size = ITEM_SIZE
        self.pos = (pos[0], pos[1])
        self.rect = self.image.get_rect(center=self.pos)
        self.lifetime = 0 # maximum wait time
        self.__set_lifetime__()
        self.effect_duration = 0
        self.__set_duration__()
        self.state = ItemState.WAITING
        self.effect = None
        self.current_user = None # stores the player that got the item, so that it may be internally restored
        self.existence_time = birth_time
        self.use_time = None

    # should define a lifetime in miliseconds for each concrete item
    def __set_lifetime__(self):
        """sets the maximum wait time of an item of a concrete type"""
        raise NotImplementedError(
            "This method is abstract and must be implemented in derived classes"
        )

    # should define a duration in miliseconds for each concrete item
    def __set_duration__(self):
        """sets the effect duration of an item of a concrete type"""
        raise NotImplementedError(
            "This method is abstract and must be implemented in derived classes"
        )
    
    # should define the concrete effect once the item is touched by a player
    def __create_effect__(self, player: Player):
        """establishes what effect the item actually causes on the player"""
        raise NotImplementedError(
            "This method is abstract and must be implemented in derived classes"
        )
    
    def update(self, time: int, players: Group) -> Player|None:
        """simple implementation of an FSM to track the item duration and lifetime, 
        and eventually restore a transformed player"""
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
        """simply checks whether a player got the item"""
        players = pygame.sprite.spritecollide(self, players, False, collided=Item.collided)
        return players[0] if len(players) != 0 else None
        
    def create_message(self, player: Player) -> Message:
        """initializes the grafical elements of the item msg to be displayed when got by a player,
        as well as stores the position where it should be drawn"""
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

# simplest way of listing the concrete types for the simulation, though
# there's probably a way of generating it metalinguistically
item_type_list = [Mushroom, Accelerator]