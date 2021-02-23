from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.comm.message_protocol import MessageProtocol
from ....core.state.state import State
from ....core.state.state import StateHandler
from ....core.comm.comm_utils import CommUtils
from ....core.config.config import Config
from time import sleep

class ConnectTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if

        self.state_def =  [
            State("CONNECT_START", self.handle_connect_start, "CONNECT_MASTERCHIEF", "CONNECT_START"),
            State("CONNECT_MASTERCHIEF", self.handle_masterchief, "CONNECT_GARRUS", "CONNECT_START"),
            State("CONNECT_GARRUS", self.handle_connect_garrus, "CONNECT_DAREDEVIL", "CONNECT_START"),
            State("CONNECT_DAREDEVIL", self.handle_connect_daredevil, "CONNECT_FEAR", "CONNECT_START"),
            State("CONNECT_FEAR", self.handle_connect_fear, "CONNECT_KRATOS", "CONNECT_START"),
            State("CONNECT_KRATOS", self.handle_connect_kratos, "ENABLED", "CONNECT_START"),
            State("ENABLED", self.handle_enabled, "ENABLED", "CONNECT_START")
        ]
        self.state_handler = StateHandler(self.state_def, "CONNECT_START")

    def run(self):
        func = self.state_handler.get_state_func()
        func()

    def handle_connect_start(self):
        self.state_handler.transition()

    def handle_masterchief(self):
        fail = False
        if False == CommUtils.is_connected(self.comm_if, "masterchief"):
            fail = True != CommUtils.connect(self.comm_if, "masterchief")
        sleep(1)
        self.state_handler.transition(fail)

    def handle_connect_garrus(self):
        fail = False
        if False == CommUtils.is_connected(self.comm_if, "garrus"):
            fail = True != CommUtils.connect(self.comm_if, "garrus")
        sleep(1)
        self.state_handler.transition(fail)

    def handle_connect_daredevil(self):
        fail = False
        if False == CommUtils.is_connected(self.comm_if, "daredevil"):
            fail = True != CommUtils.connect(self.comm_if, "daredevil")
        sleep(1)
        self.state_handler.transition(fail)

    def handle_connect_fear(self):
        fail = False
        if False == CommUtils.is_connected(self.comm_if, "fear"):
            fail = True != CommUtils.connect(self.comm_if, "fear")
        sleep(1)
        self.state_handler.transition(fail)
    
    def handle_connect_kratos(self):
        fail = False
        if False == CommUtils.is_connected(self.comm_if, "kratos"):
            fail = True != CommUtils.connect(self.comm_if, "kratos")
        sleep(1)
        self.state_handler.transition(fail)

    def handle_enabled(self):
        #Check if still connected
        connected = CommUtils.is_connected(self.comm_if, "masterchief")
        connected = connected and CommUtils.is_connected(self.comm_if, "garrus")
        connected = connected and CommUtils.is_connected(self.comm_if, "daredevil")
        connected = connected and CommUtils.is_connected(self.comm_if, "fear")
        connected = connected and CommUtils.is_connected(self.comm_if, "kratos")

        fail = False == connected
        if True == fail:
            self.state_handler.transition(fail)