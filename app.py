import pygame
from pygame.event import Event
from GUI.menu import Menu
from GUI.button import Button
from simulation import Simulation


class App:
    def __init__(self):
        self._running = True
        self._screen = None
        self.menu = Menu()
        self.background_image = pygame.image.load("resources/background.jpeg")
        self.lawn = pygame.image.load("resources/lawn.jpeg")
        self.__update_assets__()
        self.simulation = Simulation(self.menu.configs, self.lawn)
        self.button = Button()

    def draw_field(self):
        pass

    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode(self.menu.get_config("screen_res"))
        self._running = True

    def on_event(self, event: Event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        if self._running:
            self.simulation.update()
        pass

    def on_render(self):
        # Draw background
        self.__update_assets__()
        self._screen.blit(self.background_image, (0, 0))
        self._screen.blit(self.lawn, (0, self.menu.get_config("status_bar_height")))

        if self._running:
            self._screen = self.button.draw(self._screen)
            self._screen = self.simulation.draw(self._screen)
        else:
            pass
        # Update the display
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def __update_assets__(self):
        self.background_image = pygame.transform.scale(
            self.background_image, (self.menu.get_config("screen_res")[0], self.menu.get_config("status_bar_height"))
        )
        self.lawn = pygame.transform.scale(self.lawn, self.menu.get_config("field_size"))
