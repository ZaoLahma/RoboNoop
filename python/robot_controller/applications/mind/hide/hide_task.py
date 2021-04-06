from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.state.state import State
from ....core.state.state import StateHandler
from ....core.comm.comm_utils import CommUtils
from ...kratos.motor_control.motor_control_messages import MoveInd
from ...kratos.motor_control.motor_control_messages import ReleaseCtrlInd
from ...daredevil.sonar_control.sonar_control_messages import SonarDataInd

from time import time

class HideTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_init, "FIND_DIRECTION", "INIT"),
            State("FIND_DIRECTION", self.handle_find_direction, "TURN", "INIT"),
            State("TURN", self.handle_turn, None, None),
            State("MOVE", self.handle_move, "REST", "INIT"),
            State("REST", self.handle_rest, "REST", "INIT")
        ]
        self.state_handler = StateHandler(self.state_def, "INIT")

        self.turn_time = None
        self.turn_start_time = time()
        self.turn_exit_state = None

    def run(self):
        func = self.state_handler.get_state_func()
        func()

    def handle_init(self):
        self.state_handler.transition()

    def handle_find_direction(self):
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            if msg.distance > 3000:
                move_ind = MoveInd(MoveInd.LEFT, 100, 2)
                self.comm_if.send_message(move_ind)
                self.state_handler.transition()
                self.turn_start_time = time()
                self.turn_time = 0.1 #Seconds
                self.turn_exit_state = "FIND_DIRECTION"
            else:
                move_ind = MoveInd(MoveInd.FORWARD, 100, 2)
                self.comm_if.send_message(move_ind)
                self.state_handler.transition_to("MOVE")

    def handle_turn(self):
        if time() - self.turn_start_time >= self.turn_time:
            move_ind = MoveInd(MoveInd.STOP, 100, 2)
            self.comm_if.send_message(move_ind)
            self.state_handler.transition_to(self.turn_exit_state)

    def handle_move(self):
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            if msg.distance < 400:
                move_ind = MoveInd(MoveInd.RIGHT, 100, 2)
                self.comm_if.send_message(move_ind)
                self.turn_time = 0.5
                self.turn_exit_state = "REST"

    def handle_rest(self):
        release_ctrl_ind = ReleaseCtrlInd(2)
        self.comm_if.send_message(release_ctrl_ind)
        self.state_handler.transition()