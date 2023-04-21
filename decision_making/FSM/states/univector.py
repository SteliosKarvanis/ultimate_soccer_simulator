from typing import Dict
from decision_making.FSM.states.abstract_state import AbstractState
from utils.agent_actions import Action
from trajectory_planner.univector_field import UnivectorField
from math import radians
from utils.utils import polar_to_cartesian_vector
from world_state import WorldState


class UnivectorNavigate(AbstractState):
    def __init__(self) -> None:
        super().__init__()
        self.univector = UnivectorField()

    def next_state(self, world_state: WorldState) -> AbstractState:
        return self

    def run(self, world_state: WorldState) -> Action:
        ball_pose = world_state.ball_state[0], world_state.ball_state[1], 0
        obstacle = world_state.player_state[0], world_state.player_state[1]
        player_pos = world_state.opponent_state[0], world_state.opponent_state[1]
        player_vel = world_state.opponent_state[3]
        player_vel_vector = polar_to_cartesian_vector(player_vel, world_state.opponent_state[2])
        desired_angle = self.univector.compute_composed_field(ball_pose, player_pos, player_vel_vector, obstacle)
        v1 = polar_to_cartesian_vector(1, desired_angle)
        v2 = polar_to_cartesian_vector(1, radians(world_state.opponent_state[2]))
        action = Action()
        if v1[0] * v2[0] + v1[1] * v2[1] < 0:
            action.forward = -1
        else:
            action.forward = 1
        if v1[0] * v2[1] - v1[1] * v2[0] > 0:
            action.rotate = 1
        else:
            action.rotate = -1
        return action
