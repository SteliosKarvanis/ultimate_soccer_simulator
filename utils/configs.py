from dataclasses import dataclass, field
from typing import Tuple

@dataclass(frozen=True)
class Configuration:
    screen_res: Tuple[int, int] = (1280, 800)
    screen_to_field_ratio: float = field(kw_only=True, default=0.9)
    field_size: Tuple[int, int] = field(init=False)
    status_bar_height: int = field(init=False)
    
    def __post_init__(self):
        object.__setattr__(self,"field_size",(self.screen_res[0], round(self.screen_res[1]*self.screen_to_field_ratio)))
        object.__setattr__(self,"status_bar_height", self.screen_res[1]-self.field_size[1])
    
@dataclass(frozen=True)
class SimulConfig(Configuration):
    scoreboard_height: int = field(init=False)
    FPS: int = field(kw_only=True, default=60)

    def __post_init__(self):
        super().__post_init__()
        object.__setattr__(self,"scoreboard_height", round(1.5*self.status_bar_height))
    
    @classmethod
    def generate_from_config(cls, config: Configuration):
        return cls(config.screen_res, screen_to_field_ratio = config.screen_to_field_ratio)
