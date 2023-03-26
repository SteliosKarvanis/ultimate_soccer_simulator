from typing import Dict
from utils.agent_actions import Action
from decision_making.FSM.states.follow_ball import FollowBall
from decision_making.abstract_policy import AbstractBehaviour

class FSM(AbstractBehaviour):
    def __init__(self) -> None:
        super().__init__()
        self.spin_count = 0
        self.state = FollowBall()

    def get_action(self, world_state: Dict) -> Action:
        self.state = self.state.next_state(world_state)
        return self.state.run(world_state)