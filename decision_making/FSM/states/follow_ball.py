from decision_making.FSM.states.abstract_state import AbstractState
from utils.agent_actions import Action
from world_state import WorldState
from pygame.math import Vector2

FOWARD_ANGLE=5
ROTATE_ANGLE=30
class FollowBall(AbstractState):
    def __init__(self) -> None:
        super().__init__()

    def next_state(self, world_state: WorldState) -> AbstractState:
        return self

    def run(self, world_state: WorldState) -> Action:
        relative_position=Vector2(world_state.ball_pos[0]-world_state.opponent_pos[0],world_state.ball_pos[1]-world_state.opponent_pos[1])
        orientation=world_state.opponent_orientation
        xaxis=Vector2(1,0)
        angle0=(int(xaxis.angle_to(relative_position)))%360
        control_angle=(orientation-angle0)%360
        if (control_angle>=0 and control_angle<=FOWARD_ANGLE) or (control_angle<360 and control_angle>=360-FOWARD_ANGLE):
            return Action(forward=1)
        elif control_angle<=ROTATE_ANGLE:
            return Action(rotate=1,forward=1)
        elif control_angle<=180:
            return Action(rotate=1)
        elif control_angle<=360-ROTATE_ANGLE:
            return Action(rotate=-1)
        else:
            return Action(rotate=-1,forward=1)
