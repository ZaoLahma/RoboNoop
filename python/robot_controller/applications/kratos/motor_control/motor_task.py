from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.state.state import State
from ....core.state.state import StateHandler
from ...daredevil.sonar_control.sonar_control_messages import SonarDataInd

class MotorTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_init, "CONNECT_DAREDEVIL", "INIT"),
            State("CONNECT_DAREDEVIL", self.handle_connect_daredevil, "ENABLED", "INIT"),
            State("ENABLED", self.handle_enabled, "ENABLED", "INHIBITED"),
            State("AVOID_COLLISION", self.handle_avoid_collision, "ENABLED", "INHIBITED"),
            State("INHIBITED", self.handle_inhibited, "ENABLED", "INIT")
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

    def handle_enabled(self):
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            Log.log("Motor task receiving sonar data")
            if 300 > msg.distance:
                Log.log("Too close to object - avoid collision")
                self.state_handler.transition_to("AVOID_COLLISION")

    def handle_avoid_collision(self):
        Log.log("Avoiding collisions")
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            Log.log("Collision - Distance: " + str(msg.distance))
            if 300 < msg.distance:
                self.state_handler.transition()

    def handle_inhibited(self):
        Log.log("Inhibited")