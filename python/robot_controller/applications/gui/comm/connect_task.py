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
            State("CONNECT", self.handle_connect, "ENABLED", "CONNECT"),
            State("ENABLED", self.handle_enabled, "ENABLED", "CONNECT")
        ]

        self.state_handler = StateHandler(self.state_def, "CONNECT")

    def run(self):
        func = self.state_handler.get_state_func()
        func()

    def handle_connect_start(self):
        self.state_handler.transition()

    def handle_connect(self):
        fail = False
        app_config = Config.get_config_val("application")["comm"]
        for app_name in app_config:
            if False == CommUtils.is_connected(self.comm_if, app_name):
                fail = True != CommUtils.connect(self.comm_if, app_name)
                if True == fail:
                    sleep(1)
        self.state_handler.transition(fail)

    def handle_enabled(self):
        #Check if still connected
        connected = True
        app_config = Config.get_config_val("application")["comm"]
        for app_name in app_config:
            connected = connected and CommUtils.is_connected(self.comm_if, app_name)
            if False == connected:
                break

        fail = False == connected
        if True == fail:
            self.state_handler.transition(fail)