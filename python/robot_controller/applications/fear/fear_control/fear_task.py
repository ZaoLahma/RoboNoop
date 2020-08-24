from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.state.state import State
from ....core.state.state import StateHandler
from ...kratos.motor_control.motor_control_messages import MoveInd
from ...daredevil.sonar_control.sonar_control_messages import SonarDataInd
import time

class FearTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_init, "CONNECT_DAREDEVIL", "INIT"),
            State("CONNECT_DAREDEVIL", self.handle_connect_daredevil, "CONNECT_KRATOS", "INIT"),
            State("CONNECT_KRATOS", self.handle_connect_kratos, "ENABLED", "INIT"),
            State("ENABLED", self.handle_enabled, "ESCAPING", "INHIBITED"),
            State("ESCAPING", self.handle_escaping, "ENABLED", "INHIBITED")
        ]
        self.state_handler = StateHandler(self.state_def, "INIT")

    def run(self):
        func = self.state_handler.get_state_func()
        func()

    def handle_init(self):
        self.state_handler.transition()

    def handle_connect_daredevil(self):
        if False == self.comm_if.is_connected(3033):
            try:
                self.comm_if.connect("localhost", 3033)
                self.state_handler.transition()
            except Exception as e:
                Log.log("Exception when connecting to daredevil: " + str(e))
                self.state_handler.transition(fail=True)
        else:
            self.state_handler.transition()
    
    def handle_connect_kratos(self):
        if False == self.comm_if.is_connected(3031):
            try:
                self.comm_if.connect("localhost", 3031)
                self.state_handler.transition()
            except Exception as e:
                Log.log("Exception when connecting to kratos: " + str(e))
                self.state_handler.transition(fail=True)
        else:
            self.state_handler.transition()

    def handle_enabled(self):
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            Log.log("Fear task receiving sonar data in ENABLED")
            if msg.distance < 300:
                move_ind = MoveInd(MoveInd.BACKWARD, 100, 0)
                self.comm_if.send_message(move_ind)
                self.state_handler.transition()

    def handle_escaping(self):
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            Log.log("Fear task receiving sonar data in ESCAPING")
            if msg.distance > 400:
                move_ind = MoveInd(MoveInd.STOP, 100, 0)
                self.comm_if.send_message(move_ind)
                self.state_handler.transition()
            else:
                move_ind = MoveInd(MoveInd.BACKWARD, 100, 0)
                self.comm_if.send_message(move_ind)
                self.state_handler.transition()