import pygame
from pygame.event import Event
from GUI.menu import Menu
from GUI.button import Button
from simulation import Simulation
from GUI.start_menu import Start_Menu


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

    def on_init(self):
        pygame.init()
        self.text_font1 = pygame.font.SysFont(None, 80)
        self.text_font2 = pygame.font.SysFont(None, 50)
        self.start_menu = Start_Menu()
        self._screen = pygame.display.set_mode(self.menu.get_config("screen_res"))
        self._running = True

    def on_event(self, event: Event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            self.simulation.start()

    def on_loop(self):
        if self.simulation.is_running():
            self.simulation.update()

    def on_render(self):
        self.__update_assets__()
        if self._running:
            self._screen = self.button.draw(self._screen)
            if self.simulation.is_running():
                self._screen.blit(self.background_image, (0, 0))
                self._screen.blit(
                    self.lawn, (0, self.menu.get_config("status_bar_height"))
                )
                self._screen = self.simulation.draw(self._screen)
            else:
                self._screen.blit(
                    pygame.transform.scale(self.lawn, self._screen.get_size()), (0, 0)
                )
                text1 = self.text_font1.render(
                    self.start_menu.text1, True, self.start_menu.text_color
                )
                text2 = self.text_font2.render(
                    self.start_menu.text2, True, self.start_menu.text_color
                )
                text3 = self.text_font2.render(
                    self.start_menu.text3, True, self.start_menu.text_color
                )
                text4 = self.text_font2.render(
                    self.start_menu.text4, True, self.start_menu.text_color
                )
                self._screen.blit(
                    text1,
                    (self._screen.get_width() / 20, self._screen.get_height() / 4),
                )
                self._screen.blit(
                    text3,
                    (self._screen.get_width() / 10, self._screen.get_height() / 2),
                )
                self._screen.blit(
                    text4,
                    (self._screen.get_width() / 10, self._screen.get_height() / 2 + 50),
                )
                self._screen.blit(
                    text2,
                    (self._screen.get_width() / 10, self._screen.get_height() * 2 / 3),
                )
        else:
            pass
        # Update the display
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def __update_assets__(self):
        self.background_image = pygame.transform.scale(
            self.background_image,
            (
                self.menu.get_config("screen_res")[0],
                self.menu.get_config("status_bar_height"),
            ),
        )
        self.lawn = pygame.transform.scale(
            self.lawn, self.menu.get_config("field_size")
        )
