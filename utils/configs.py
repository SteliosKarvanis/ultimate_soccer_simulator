from dataclasses import dataclass, field
from typing import Tuple

FPS = 120
SAMPLE_TIME = 1 / FPS
INITIAL_SCREEN_WIDTH = 1200
INITIAL_SCREEN_HEIGHT = 900
INITIAL_SCREEN_SIZE = (INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT)


@dataclass(frozen=True)
class Configuration:
    """stores some possibly configurable attributes related to the app, 
    its fields are immutable to prevent configurations from changing at an innapropriate moment,
    therefore, if a configuration field should ever be changed by the app, a new Configuration object should be created"""
    screen_res: Tuple[int, int] = INITIAL_SCREEN_SIZE
    screen_to_field_ratio: float = field(kw_only=True, default=0.9)
    field_size: Tuple[int, int] = field(init=False)
    status_bar_height: int = field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self, "field_size", (self.screen_res[0], round(self.screen_res[1] * self.screen_to_field_ratio))
        )
        object.__setattr__(self, "status_bar_height", self.screen_res[1] - self.field_size[1])


@dataclass(frozen=True)
class SimulConfig(Configuration):
    """
    adds fields that are only relevant to the simulation
    """
    scoreboard_height: int = field(init=False)
    FPS: int = field(kw_only=True, default=FPS)

    def __post_init__(self):
        super().__post_init__()
        object.__setattr__(self, "scoreboard_height", round(1.5 * self.status_bar_height))

    @classmethod
    def generate_from_config(cls, config: Configuration):
        return cls(config.screen_res, screen_to_field_ratio=config.screen_to_field_ratio)
