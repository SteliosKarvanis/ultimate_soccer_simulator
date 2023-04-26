import pygame
from pygame.event import Event
from GUI.menu import Menu
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

    def on_init(self):
        """transitions from initial state to running and initializes some graphical attributes, including the screen"""
        pygame.init()
        self.title_font = pygame.font.SysFont('Times New Roman', 57, bold=True)
        self.normal_font = pygame.font.SysFont('Arial', 40, bold=True)
        self._screen = pygame.display.set_mode(self.menu.get_config("screen_res"))
        self._running = True

    def on_event(self, event: Event):
        """detects key presses related to extra game events i.e. pausing, restarting and quitting"""
        if event.type == pygame.QUIT:
            self._running = False
            return

        if self.simulation.is_running() and event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_p:
                    if self.simulation.is_paused():
                        self.simulation.play()
                    else:
                        self.simulation.pause()
                
                case pygame.K_r:
                    self.simulation.start()
                
                case pygame.K_BACKSPACE:
                    self.simulation.running = False

        if event.type == pygame.KEYDOWN and not self.simulation.is_running() and event.key != pygame.K_BACKSPACE:
            self.simulation.start()

    def on_loop(self):
        """serves only to update the simulation state when it's in the running and playing state"""
        if self.simulation.is_running() and not self.simulation.is_paused():
            self.simulation.update()

    def on_render(self):
        """draws the assets to the screen according to the simulation state"""
        self.__update_assets__()
        if self._running:
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
                title_start = self.title_font.render(
                    self.menu.title[0], True, self.menu.text_color
                )
                game_title = self.title_font.render(
                    self.menu.title[1], True, self.menu.title_color
                )
                self._screen.blit(title_start,(self._screen.get_width() / 20, self._screen.get_height()/4))
                self._screen.blit(game_title,(self._screen.get_width() / 20 + title_start.get_width() + self.normal_font.get_height()/2, self._screen.get_height()/4))
                pos_y = self._screen.get_height()/2
                pos_x = self._screen.get_width()/2
                for text in self.menu.texts:
                    text = self.normal_font.render(text, True, self.menu.text_color)
                    pos_y += self.normal_font.get_height()*1.5
                    self._screen.blit(text,(pos_x - text.get_width()/2, pos_y))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        """implements the flow control of the general app states (initializing, running or quitting)"""
        self.on_init()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def __update_assets__(self):
        """updates the graphical elements in accordance with the current window size and other related configuration fields"""
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
