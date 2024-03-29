from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.state.state import State
from ....core.state.state import StateHandler
from ....core.comm.comm_utils import CommUtils
from ...kratos.motor_control.motor_control_messages import MoveInd
from ...kratos.motor_control.motor_control_messages import ReleaseCtrlInd
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
        fail = True != CommUtils.connect(self.comm_if, "daredevil")
        self.state_handler.transition(fail)
    
    def handle_connect_kratos(self):
        fail = True != CommUtils.connect(self.comm_if, "kratos")
        self.state_handler.transition(fail)

    def handle_enabled(self):
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            #Log.log("Fear task receiving sonar data in ENABLED")
            if msg.distance < 300:
                move_ind = MoveInd(MoveInd.BACKWARD, 100, 0)
                self.comm_if.send_message(move_ind)
                self.state_handler.transition()

    def handle_escaping(self):
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            Log.log("Fear task receiving sonar data in ESCAPING")
            if msg.distance > 400:
                release_ctrl_ind = ReleaseCtrlInd(0)
                self.comm_if.send_message(release_ctrl_ind)
                self.state_handler.transition()