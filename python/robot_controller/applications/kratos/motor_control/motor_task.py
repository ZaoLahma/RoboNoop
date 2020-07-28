from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.state.state import State
from ....core.state.state import StateHandler
from ...daredevil.sonar_control.sonar_control_messages import SonarDataInd

class MotorTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_init, "ENABLED", "INIT"),
            State("ENABLED", self.handle_enabled, "ENABLED", "INHIBITED"),
            State("AVOID_COLLISION", self.handle_avoid_collision, "ENABLED", "INHIBITED"),
            State("INHIBITED", self.handle_inhibited, "ENABLED", "INIT")
        ]

        self.state_handler = StateHandler(self.state_def, "INIT")

    def run(self):
        Log.log("Run called")
        func = self.state_handler.get_state_func()
        func()

    def handle_init(self):
        self.state_handler.transition()

    def handle_enabled(self):
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())

    def handle_avoid_collision(self):
        Log.log("Avoiding collisions")

    def handle_inhibited(self):
        Log.log("Inhibited")