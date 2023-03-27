from abc import ABC, abstractmethod
from typing import Dict
from utils.agent_actions import Action
from world_state import WorldState


class AbstractState(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def next_state(self, world_state: WorldState):
        pass

    @abstractmethod
    def run(self, world_state: WorldState) -> Action:
        pass
