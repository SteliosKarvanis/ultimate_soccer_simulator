from utils.configs import Configuration
from pygame.colordict import THECOLORS as colors

class Menu:
    def __init__(self) -> None:
        self.configs = Configuration()
        self.title = "Welcome to", "THE Ultimate Soccer Simulator!"
        self.texts = [
            "To navigate the player use the arrow keys",
            "Press 'p' to pause/play",
            "Press 'r' to restart the game at any moment",
            "Press <backspace> to return to this title screen",
            "or press any key to start the game!",
        ]
        self.title_color = colors.get("blue")
        self.text_color = colors.get("white")

    def get_config(self, field: str):
        return getattr(self.configs, field)
