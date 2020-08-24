from ...core.state.state import State
from ...core.state.state import StateHandler
from ...core.runtime.task_base import TaskBase
from ...core.runtime.process import ProcessManager
from ..kratos.main import Main as KratosMain
from ..daredevil.main import Main as DaredevilMain
from ..garrus.main import Main as GarrusMain
from ..fear.main import Main as FearMain

from ...core.log.log import Log
from datetime import datetime

class MasterChief(TaskBase):
    def __init__(self, comm_if):
        TaskBase.__init__(self)

        self.process_manager = ProcessManager()

        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_init, "CONNECT_DAREDEVIL", "INIT"),
            State("IDLE", self.handle_idle, "CONNECT_DAREDEVIL", "IDLE"),
            State("CONNECT_DAREDEVIL", self.handle_connect_daredevil, "CONNECT_FEAR", "START_PROCESSES"),
            State("CONNECT_FEAR", self.handle_connect_fear, "CONNECT_KRATOS", "START_PROCESSES"),
            State("CONNECT_KRATOS", self.handle_connect_kratos, "ENABLED", "START_PROCESSES"),
            State("CONNECT_GARRUS", self.handle_connect_garrus, "ENABLED", "START_PROCESSES"),
            State("START_PROCESSES", self.handle_start_processes, "IDLE", "DISABLED"),
            State("ENABLED", self.handle_enabled, "NO_STATE", "NO_STATE"),
            State("DISABLED", self.handle_disabled, "NO_STATE", "NO_STATE")
        ]

        self.state_handler = StateHandler(self.state_def, "INIT")

        self.idle_wait_ms = 1000
        self.timestamp = None
        self.num_reattempts = 0
        self.processes_to_start = []

    def run(self):
        state_func = self.state_handler.get_state_func()
        state_func()

    def handle_init(self):
        self.comm_if.publish_service(3030)
        self.state_handler.transition()

    def handle_idle(self):
        if self.timestamp == None:
            self.timestamp = datetime.now()
        time_delta = datetime.now() - self.timestamp
        elapsed_ms = time_delta.total_seconds() * 1000
        if elapsed_ms >= self.idle_wait_ms:
            self.timestamp = None
            self.state_handler.transition()

    def handle_connect_kratos(self):
        if False == self.comm_if.is_connected(3031):
            try:
                self.comm_if.connect("localhost", 3031)
                self.state_handler.transition()
            except Exception as e:
                Log.log("Exception when connecting to kratos: " + str(e))
                self.processes_to_start.append(("KratosProcess", KratosMain.run))
                self.state_handler.transition(fail=True)
        else:
            self.state_handler.transition()

    def handle_connect_daredevil(self):
        if False == self.comm_if.is_connected(3033):
            try:
                self.comm_if.connect("localhost", 3033)
                self.state_handler.transition()
            except Exception as e:
                Log.log("Exception when connecting to daredevil: " + str(e))
                self.processes_to_start.append(("DaredevilProcess", DaredevilMain.run))
                self.state_handler.transition(fail=True)
        else:
            self.state_handler.transition()

    def handle_connect_fear(self):
        if False == self.comm_if.is_connected(3034):
            try:
                self.comm_if.connect("localhost", 3034)
                self.state_handler.transition()
            except Exception as e:
                Log.log("Exception when connecting to fear: " + str(e))
                self.processes_to_start.append(("FearProcess", FearMain.run))
                self.state_handler.transition(fail=True)
        else:
            self.state_handler.transition()

    def handle_connect_garrus(self):
        if False == self.comm_if.is_connected(3032):
            try:
                self.comm_if.connect("localhost", 3032)
                self.state_handler.transition()
            except Exception as e:
                Log.log("Exception when connecting to garrus: " + str(e))
                self.processes_to_start.append(("GarrusProcess", GarrusMain.run))
                self.state_handler.transition(fail=True)
        else:
            self.state_handler.transition()

    def handle_start_processes(self):
        for process in self.processes_to_start:
            try:
                self.process_manager.start_process(process[0], process[1])
            except Exception as e:
                Log.log("Exception when starting " + process[0] + ": " + str(e))
        self.processes_to_start = []
        self.state_handler.transition()

    def handle_enabled(self):
        if False == self.comm_if.is_connected(3033):
            Log.log("Lost connection to Daredevil")
        if False == self.comm_if.is_connected(3031):
            Log.log("Lost connection to Kratos")

    def handle_disabled(self):
        Log.log("Disabled...")
