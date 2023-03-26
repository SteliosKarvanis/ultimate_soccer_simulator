from typing import Dict
from abc import ABC
from utils.agent_actions import Action

class AbstractBehaviour(ABC):
    def __init__(self) -> None:
        super().__init__()

    def get_action(self, world_state: Dict) -> Action:
        return Action(rotate=1, forward=0, spin=0)