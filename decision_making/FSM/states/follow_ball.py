from typing import Dict
from decision_making.FSM.states.abstract_state import AbstractState
from utils.agent_actions import Action

class FollowBall(AbstractState):
    def __init__(self) -> None:
        super().__init__()
    
    def next_state(self, world_state: Dict):
        pass
    
    def run(self, world_state: Dict) -> Action:
        action = Action()
        action.forward = 1
        action.rotate = 1
        return action        