import pygame
from constants import *
from GUI.player import Player

class App:
    def __init__(self):
        self._running = True
        self._screen = None
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT
        self.player = Player()
 
    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode(self.size)
        self._running = True
 

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.K_SPACE:
            self._running = False


    def on_loop(self):
        #TODO
        pass


    def on_render(self):
        self._screen.fill(BACKGROUND_COLOR)
        player_surface, player_pos = self.player.draw_player()
        self._screen.blit(source=player_surface, dest=player_pos)
        # Update the display
        pygame.display.flip()
        #TODO
        pass


    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            keys_pressed = pygame.key.get_pressed()
            self.player.actions(keys_pressed)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 