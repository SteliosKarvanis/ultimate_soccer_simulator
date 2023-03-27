from typing import Dict
from decision_making.FSM.states.abstract_state import AbstractState
from utils.agent_actions import Action
from trajectory_planner.univector_field import UnivectorField
from math import pi
from world_state import WorldState


class UnivectorNavigate(AbstractState):
    def __init__(self) -> None:
        super().__init__()
        self.univector = UnivectorField()

    def next_state(self, world_state: WorldState) -> AbstractState:
        return self

    def run(self, world_state: WorldState) -> Action:
        ball_pose = world_state.ball_pos[0], world_state.ball_pos[1], 0
        desired_angle = self.univector.compute_move_to_goal_field(ball_pose, world_state.opponent_pos)
        action = Action(forward=1)
        current_angle = world_state.player_orientation * pi / 180
        tolerance = 10
        if desired_angle > current_angle + tolerance:
            action.rotate = 1
        else:
            action.rotate = -1
        return action
