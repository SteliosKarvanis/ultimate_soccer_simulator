from typing import Tuple
import pygame
from pygame import Surface
from pygame.colordict import THECOLORS as colors
from GUI.scoreboard import ScoreBoard
from game_elements.abstract_element import AbstractElement
from game_elements.field import FIELD_LENGTH_Y, FIELD_LENGTH_X, FIELD_POINTS, LEFT_FRONT_GOAL_X
from game_elements.player import Player
from game_elements.ball import Ball
from decision_making.manual_policy import ManualBehaviour
from decision_making.FSM.fsm_policy import FSM
from utils.configs import Configuration, SimulConfig
from utils.utils import reflect_vector_vertically, translate_vector
from world_state import WorldState
from game_elements.item import *
from utils.collision_handler import CollisionHandler
import random

MARGIN = 16
LINE_THICKNESS = 5

class Simulation:
    def __init__(self, config: Configuration, surface: Surface) -> None:
        self.configs = SimulConfig.generate_from_config(config)
        self.surface = surface
        self.scoreboard = ScoreBoard(self.configs.scoreboard_height)
        self.FPS = self.configs.FPS
        self.collision_handler = CollisionHandler(self.generate_scaling_function())
        self.ally = Player(
            "resources/player.png",
            behaviour=ManualBehaviour(),
        )
        self.opponent = Player(
            "resources/opponent.png",
            initial_pos=(-LEFT_FRONT_GOAL_X / 2, 0),
            behaviour=FSM(),
        )
        self.players = pygame.sprite.Group(self.ally, self.opponent)
        self.__initialize_player_sprites__()
        self.ball = Ball()
        self.game_elements = pygame.sprite.Group(self.ally, self.opponent, self.ball)
        self.active_items = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.clock.tick()

    def update(self):
        if not self.ball.collision_management(self.ally):
            l = self.ball.collision_management(self.opponent)
        goal_state = self.ball.update()
        if goal_state != "None":
            self.scoreboard.update(character=goal_state, frame_height=self.configs.scoreboard_height)
        if self.scoreboard.half_minute_passed():
            self.generate_item()

        for item in self.active_items:
            assert isinstance(item, Item)
            player = item.update(self.clock.get_time(), self.players)
            if player != None:
                item.effect.transform(player)
        self.ally.update(self.get_state(), self.collision_handler)
        self.opponent.update(self.get_state(), self.collision_handler)

    def draw(self, screen: Surface) -> Surface:
        screen = self.draw_field(screen)
        screen = self.__draw_elements__(screen)
        screen = self.__draw_items__(screen)
        screen = self.scoreboard.draw(screen, self.clock.tick())
        return screen

    def get_state(self) -> WorldState:
        return WorldState(
            player_state=self.ally.get_state(),
            opponent_state=self.opponent.get_state(),
            ball_state=self.ball.get_state(),
        )

    def generate_item(self):
        pos = (random.uniform(-FIELD_LENGTH_X/4,FIELD_LENGTH_X/4), random.uniform(-FIELD_LENGTH_Y/4, FIELD_LENGTH_Y/4))
        new_item_type = random.sample(item_type_list, 1)
        new_item_type = new_item_type[0]
        new_item = new_item_type(pos, self.clock.get_time())
        self.initialize_item(new_item)
        self.active_items.add(new_item)
        
    def initialize_item(self, item: Item):
        item.size = self.field_to_pix_scale(item.size)
        item.pos = self.field_to_pix_scale(item.pos)
        item.image = pygame.transform.scale(item.image, item.size)
        item.mask = pygame.mask.from_surface(item.image)
        item.rect = item.image.get_rect(center=item.pos)
        print(item.pos)
        

    def __draw_elements__(self, screen: Surface) -> Surface:
        for sprite in self.game_elements.sprites():
            screen = self.__draw_element__(screen, sprite)
        return screen

    def __draw_element__(self, screen: Surface, element: AbstractElement) -> Surface:
        surface = pygame.transform.scale(element.get_surface(), self.field_to_pix_scale(element.size))
        sprite = pygame.transform.rotate(surface, element.get_orientation())
        rect = sprite.get_rect()
        rect.center = self.field_to_pix_coord(element.get_pos())
        screen.blit(source=sprite, dest=rect)
        return screen
    
    def __draw_items__(self, screen: Surface)-> Surface:
        for item in self.active_items:
            if item.lifetime > 0:
                screen.blit(source=item.image, dest=item.image.get_rect(center=self.field_to_pix_coord(item.pos, scale=False)))
        return screen

    def field_to_pix_coord(self, point_field: Tuple[float, float], scale = True) -> Tuple[int, int]:
        if scale:
            point_field = self.field_to_pix_scale(point_field)
        point = reflect_vector_vertically(point_field)
        point = translate_vector(point, self.get_field_center())
        return point

    def get_field_center(self) -> Tuple[float, float]:
        center = pygame.display.get_surface().get_size()
        return center[0] / 2, center[1] / 2 + self.scoreboard.frame.get_height() / 2

    def draw_field(self, screen: Surface) -> Surface:
        field_points = [self.field_to_pix_coord(x) for x in FIELD_POINTS]
        pygame.draw.lines(
            surface=screen, color=pygame.Color("white"), closed=True, points=field_points, width=LINE_THICKNESS
        )
        return screen
    def __initialize_player_sprites__(self):
        self.collision_handler.update_element_sprite(self.ally)
        self.collision_handler.update_element_sprite(self.opponent)

    def generate_scaling_function(self):
        return lambda x: self.field_to_pix_scale_generic(x, self.configs.screen_res[1], self.scoreboard.frame.get_height())
    
    def field_to_pix_scale_generic(self, point, height, offset):
        field_y_pix = height - offset - 2 * MARGIN
        scale = field_y_pix / FIELD_LENGTH_Y
        return int(point[0] * scale), int(point[1] * scale)
    
    def field_to_pix_scale(self, point):
        return self.field_to_pix_scale_generic(point, pygame.display.get_surface().get_height(), self.scoreboard.frame.get_height())
