from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.comm.message_protocol import MessageProtocol
from ....core.state.state import State
from ....core.state.state import StateHandler
from ....core.comm.comm_utils import CommUtils

class CommListenerTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_init, "CONNECT_MASTERCHIEF", "INIT"),
            State("CONNECT_MASTERCHIEF", self.handle_masterchief, "CONNECT_DAREDEVIL", "INIT"),
            State("CONNECT_DAREDEVIL", self.handle_connect_daredevil, "CONNECT_FEAR", "INIT"),
            State("CONNECT_FEAR", self.handle_connect_fear, "CONNECT_KRATOS", "INIT"),
            State("CONNECT_KRATOS", self.handle_connect_kratos, "ENABLED", "INIT"),
            State("ENABLED", self.handle_enabled, "ESCAPING", "INHIBITED")
        ]
        self.state_handler = StateHandler(self.state_def, "INIT")

    def handle_init(self):
        self.state_handler.transition()

    def run(self):
        func = self.state_handler.get_state_func()
        func()

    def handle_masterchief(self):
        fail = True != CommUtils.connect(self.comm_if, "localhost", 3030, "masterchief")
        Log.log("fail: " + str(fail))
        self.state_handler.transition(fail)

    def handle_connect_daredevil(self):
        fail = True != CommUtils.connect(self.comm_if, "localhost", 3033, "daredevil")
        self.state_handler.transition(fail)

    def handle_connect_fear(self):
        fail = True != CommUtils.connect(self.comm_if, "localhost", 3034, "fear")
        self.state_handler.transition(fail)
    
    def handle_connect_kratos(self):
        fail = True != CommUtils.connect(self.comm_if, "localhost", 3031, "kratos")
        self.state_handler.transition(fail)

    def handle_enabled(self):
        return