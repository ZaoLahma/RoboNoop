from ...core.state.state import State
from ...core.state.state import StateHandler
from ...core.runtime.task_base import TaskBase

from ...core.log.log import Log
from datetime import datetime

class MasterChief(TaskBase):
    def __init__(self, comm_if):
        TaskBase.__init__(self)

        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_idle, "CONNECT_KRATOS", "INIT"),
            State("CONNECT_KRATOS", self.handle_connect_kratos, "KRATOS_CONNECTED", "INIT"),
            State("KRATOS_CONNECTED", self.handle_idle, "CONNECT_GARRUS", "INIT"),
            State("CONNECT_GARRUS", self.handle_connect_garrus, "ENABLED", "KRATOS_CONNECTED"),
            State("ENABLED", self.handle_enabled, "NO_STATE", "NO_STATE")
        ]

        self.state_handler = StateHandler(self.state_def, "INIT")

        self.idle_wait_ms = 0
        self.timestamp = None

    def run(self):
        state_func = self.state_handler.get_state_func()
        state_func()

    def handle_idle(self):
        if self.timestamp == None:
            self.timestamp = datetime.now()
        time_delta = datetime.now() - self.timestamp
        elapsed_ms = time_delta.total_seconds() * 1000
        if elapsed_ms >= self.idle_wait_ms:
            self.timestamp = None
            self.state_handler.transition()

    def handle_connect_kratos(self):
        try:
            self.comm_if.connect("localhost", 3030)
            self.state_handler.transition()
        except Exception as e:
            Log.log("Exception when connecting to kratos: " + str(e))
            self.idle_wait_ms = 1000
            self.state_handler.transition(fail=True)

    def handle_connect_garrus(self):
        try:
            self.comm_if.connect("localhost", 3031)
            self.state_handler.transition()
        except Exception as e:
            Log.log("Exception when connecting to garrus: " + str(e))
            self.state_handler.transition(fail=True)

    def handle_enabled(self):
        Log.log("Enabled...")
