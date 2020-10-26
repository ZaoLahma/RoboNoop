from ...core.state.state import State
from ...core.state.state import StateHandler
from ...core.runtime.task_base import TaskBase
from ...core.runtime.process import ProcessManager
from ...core.config.config import Config
from ...core.comm.comm_utils import CommUtils
from ..kratos.main import Main as KratosMain
from ..daredevil.main import Main as DaredevilMain
from ..garrus.main import Main as GarrusMain
from ..fear.main import Main as FearMain
from ..conn_aggregator.main import Main as ConnAggregatorMain

from ...core.log.log import Log
from datetime import datetime

class MasterChief(TaskBase):
    def __init__(self, comm_if):
        TaskBase.__init__(self)

        self.process_manager = ProcessManager()

        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_init, "CONNECT_DAREDEVIL", "INIT"),
            State("IDLE", self.handle_idle, "CONNECT_CONN_AGGREGATOR", "IDLE"),
            State("CONNECT_CONN_AGGREGATOR", self.handle_connect_conn_aggregator, "CONNECT_DAREDEVIL", "START_PROCESSES"),
            State("CONNECT_DAREDEVIL", self.handle_connect_daredevil, "CONNECT_FEAR", "START_PROCESSES"),
            State("CONNECT_FEAR", self.handle_connect_fear, "CONNECT_KRATOS", "START_PROCESSES"),
            State("CONNECT_KRATOS", self.handle_connect_kratos, "CONNECT_GARRUS", "START_PROCESSES"),
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
        app_config = Config.get_config_val("application")
        port_no = app_config["comm"]["masterchief"]["port-no"]
        self.comm_if.publish_service(port_no)
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
        fail = True != CommUtils.connect(self.comm_if, "kratos")
        if True == fail:
            self.processes_to_start.append(("KratosProcess", KratosMain.run))
        self.state_handler.transition(fail)

    def handle_connect_daredevil(self):
        fail = True != CommUtils.connect(self.comm_if, "daredevil")
        if True == fail:
            self.processes_to_start.append(("DaredevilProcess", DaredevilMain.run))
        self.state_handler.transition(fail)

    def handle_connect_fear(self):
        fail = True != CommUtils.connect(self.comm_if, "fear")
        if True == fail:
            self.processes_to_start.append(("FearProcess", FearMain.run))
        self.state_handler.transition(fail)

    def handle_connect_garrus(self):
        fail = True != CommUtils.connect(self.comm_if, "garrus")
        if True == fail:
            self.processes_to_start.append(("GarrusProcess", GarrusMain.run))
        self.state_handler.transition(fail)

    def handle_connect_conn_aggregator(self):
        fail = True != CommUtils.connect(self.comm_if, "conn_aggregator")
        if True == fail:
            self.processes_to_start.append(("ConnAggregatorProcess", ConnAggregatorMain.run))
        self.state_handler.transition(fail)

    def handle_start_processes(self):
        for process in self.processes_to_start:
            try:
                Log.log("Starting process: " + process[0])
                self.process_manager.start_process(process[0], process[1])
            except Exception as e:
                Log.log("Exception when starting " + process[0] + ": " + str(e))
        self.processes_to_start = []
        self.state_handler.transition()

    def handle_enabled(self):
        return None

    def handle_disabled(self):
        Log.log("Disabled...")
