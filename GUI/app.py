import pygame
from constants import *
from GUI.simulation import Simulation
from GUI.button import Button


class App:
    def __init__(self):
        self._running = True
        self._screen = None
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT
        self.background_image = pygame.image.load("resources/lawn.jpeg")
        self.simulation = Simulation()
        self.button = Button()

    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode(self.size)
        self._running = True
 

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False


    def on_loop(self):
        if self._running:
            self.simulation.update()
        pass


    def on_render(self):
        self.background_image = pygame.transform.scale(self.background_image, self.size)
        self._screen.blit(self.background_image, (0, 0))
        if self._running:
            self.simulation.draw()
        else:
            pass
        # Update the display
        pygame.display.flip()


    def on_cleanup(self):
        pygame.quit()


    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 