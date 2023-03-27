from utils.configs import Configuration

# from typing import Tuple
from dataclasses import fields


class Menu:
    def __init__(self) -> None:
        self.configs = Configuration()

    def get_config(self, field: str):
        return getattr(self.configs, field)
