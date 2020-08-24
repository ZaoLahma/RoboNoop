from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.state.state import State
from ....core.state.state import StateHandler
from .motor_controller import MotorController
from .motor_control_messages import MoveInd
import time

class MotorTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_init, "ENABLED", "INIT"),
            State("ENABLED", self.handle_enabled, "ENABLED", "INHIBITED")
        ]
        self.state_handler = StateHandler(self.state_def, "INIT")

        self.motor_controller = MotorController()

        self.curr_sub_system = 0xffffffff

    def run(self):
        func = self.state_handler.get_state_func()
        Log.log("Run called " + self.state_handler.curr_state.state_name)
        func()

    def handle_init(self):
        self.state_handler.transition()

    def handle_enabled(self):
        msg = self.comm_if.get_message(MoveInd.get_msg_id())
        if None != msg:
            Log.log("Motor task received message {0}".format(msg.get_msg_id()))
            if MoveInd.get_msg_id() == msg.get_msg_id():
                if msg.sub_system < self.curr_sub_system:
                    self.curr_sub_system = msg.sub_system
                    if MoveInd.STOP == msg.direction:
                        self.motor_controller.stop()
                        self.curr_sub_system = 0xffffffff
                    elif MoveInd.FORWARD == msg.direction:
                        self.motor_controller.forward()
                    elif MoveInd.LEFT == msg.direction:
                        self.motor_controller.turn_left()
                    elif MoveInd.RIGHT == msg.direction:
                        self.motor_controller.turn_right()
                    elif MoveInd.BACKWARD == msg.direction:
                        self.motor_controller.backward()
