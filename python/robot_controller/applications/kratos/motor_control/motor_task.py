from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.state.state import State
from ....core.state.state import StateHandler
from .motor_controller import MotorController
from .motor_control_messages import UnlockInd
from .motor_control_messages import MoveInd
from .motor_control_messages import ReleaseCtrlInd
import time

class MotorTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_init, "ENABLED", "INIT"),
            State("ENABLED", self.handle_enabled, "ENABLED", "INHIBITED"),
            State("INHIBITED", self.handle_inhibited, "ENABLED", "INHIBITED")
        ]
        self.state_handler = StateHandler(self.state_def, "INIT")

        self.motor_controller = MotorController()

        self.ctrl_sub_system = [0xffffffff]

    def run(self):
        func = self.state_handler.get_state_func()
        func()

    def handle_init(self):
        self.state_handler.transition()

    def insert_if_not_present(self, sub_system):
        if not sub_system in self.ctrl_sub_system:
            index = 0
            for ss in self.ctrl_sub_system:
                if sub_system < ss:
                    self.ctrl_sub_system.insert(index, sub_system)
                index += 1

    def handle_enabled(self):
        Log.log("ctrl_sub_system {0}".format(self.ctrl_sub_system))
        msg = self.comm_if.get_message(MoveInd.get_msg_id())
        if None != msg:
            Log.log("Motor task received MoveInd")
            self.insert_if_not_present(msg.sub_system)
            if msg.sub_system == self.ctrl_sub_system[0]:
                if MoveInd.STOP == msg.direction:
                    self.motor_controller.stop()
                elif MoveInd.FORWARD == msg.direction:
                    self.motor_controller.forward()
                elif MoveInd.LEFT == msg.direction:
                    self.motor_controller.turn_left()
                elif MoveInd.RIGHT == msg.direction:
                    self.motor_controller.turn_right()
                elif MoveInd.BACKWARD == msg.direction:
                    self.motor_controller.backward()

        msg = self.comm_if.get_message(ReleaseCtrlInd.get_msg_id())
        if None != msg:
            Log.log("Motor task received ReleaseCtrlInd " + str(msg.sub_system))
            if msg.sub_system == self.ctrl_sub_system[0]:
                self.comm_if.invalidate_messages()
                self.motor_controller.stop()
            if msg.sub_system in self.ctrl_sub_system:
                self.ctrl_sub_system.remove(msg.sub_system)

    def handle_inhibited(self):
        self.motor_controller.stop()
        msg = self.comm_if.get_message(UnlockInd.get_msg_id())
        if None != msg:
            Log.log("Unlocking robot, motion allowed")
            self.state_handler.transition()