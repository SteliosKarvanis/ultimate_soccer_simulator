import pygame
from pygame.event import Event
from GUI.menu import Menu
from simulation import Simulation
from GUI.button import Button


class App:
    def __init__(self):
        self._running = True
        self._screen = None
        self.menu = Menu()
        self.background_image = pygame.image.load("resources/background.jpeg")
        self.lawn = pygame.image.load("resources/lawn.jpeg")
        self.field = self.lawn
        self.grass = self.lawn
        self.on_init()
        self.__update_assets__()
        self.simulation = Simulation(self.menu.configs, self.field)
        self.button = Button()

    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode(self.menu.get_config("screen_res"))
        self.lawn = pygame.transform.scale(self.lawn, self.menu.get_config("field_size"))
        self._screen.blit(
            self.lawn,
            (
                0,
                self.menu.get_config("status_bar_height"),
            ),
        )
        self.background_image = pygame.transform.scale(
            self.background_image,
            (
                self.menu.get_config("screen_res")[0],
                self.menu.get_config("status_bar_height"),
            ),
        )
        self._screen.blit(self.background_image, (0, 0))
        self.background_image = self._screen.subsurface((0, 0), self.background_image.get_size())
        self.grass = self.lawn
        self.lawn = self._screen.subsurface((0, self.menu.get_config("status_bar_height")), self.lawn.get_size())
        self.field = self.lawn.subsurface((0, 0), self.lawn.get_size())
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
        if self._running:
            self._screen = self.button.draw(self._screen)
            self.simulation.draw()
        else:
            pass
        # Update the display
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def __update_assets__(self):
        self._screen.blit(
            self.grass,
            (
                0,
                self.menu.get_config("status_bar_height"),
            ),
        )
