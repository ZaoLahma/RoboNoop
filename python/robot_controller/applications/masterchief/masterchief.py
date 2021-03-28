from ...core.state.state import State
from ...core.state.state import StateHandler
from ...core.runtime.task_base import TaskBase
from ...core.runtime.process import ProcessManager
from ...core.config.config import Config
from ...core.comm.comm_utils import CommUtils
from ..kratos.main import Main as KratosMain
from ..daredevil.main import Main as DaredevilMain
from ..garrus.main import Main as GarrusMain
from ..vision.main import Main as VisionMain
from ..mind.main import Main as MindMain
from ..hwal.main import Main as HwalMain

from ...core.log.log import Log
from datetime import datetime

class MasterChief(TaskBase):
    def __init__(self, comm_if):
        TaskBase.__init__(self)

        self.process_manager = ProcessManager()

        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_init, "CONNECT", "INIT"),
            State("IDLE", self.handle_idle, "CONNECT", "IDLE"),
            State("CONNECT", self.handle_connect, "ENABLED", "START_PROCESSES"),
            State("START_PROCESSES", self.handle_start_processes, "IDLE", "DISABLED"),
            State("ENABLED", self.handle_enabled, "ENABLED", "IDLE"),
            State("DISABLED", self.handle_disabled, "NO_STATE", "NO_STATE")
        ]

        self.state_handler = StateHandler(self.state_def, "INIT")

        self.idle_wait_ms = 2000
        self.timestamp = None
        self.num_reattempts = 0
        self.processes_to_start = []

        self.app_to_main_map = {}
        self.app_to_main_map["hwal"] = HwalMain
        self.app_to_main_map["garrus"] = GarrusMain
        self.app_to_main_map["vision"] = VisionMain
        self.app_to_main_map["daredevil"] = DaredevilMain
        self.app_to_main_map["mind"] = MindMain
        self.app_to_main_map["kratos"] = KratosMain

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

    def handle_connect(self):
        fail = False
        app_config = Config.get_config_val("application")["comm"]
        for app_name in app_config:
            if False == CommUtils.is_connected(self.comm_if, app_name):
                fail = True != CommUtils.connect(self.comm_if, app_name)
                if True == fail:
                    self.processes_to_start.append((app_name + "_Process", self.app_to_main_map[app_name].run))
                    
        self.state_handler.transition(fail)

    def handle_start_processes(self):
        fail = False
        for process in self.processes_to_start:
            try:
                Log.log("Starting process: " + process[0])
                self.process_manager.start_process(process[0], process[1])
            except Exception as e:
                Log.log("Exception when starting " + process[0] + ": " + str(e))
                fail = True
        self.processes_to_start = []
        self.state_handler.transition(fail)

    def handle_enabled(self):
        fail = False
        app_config = Config.get_config_val("application")["comm"]
        for app_name in app_config:
            if False == CommUtils.is_connected(self.comm_if, app_name):
                fail = True
                break
        self.state_handler.transition(fail)

    def handle_disabled(self):
        Log.log("Disabled...")
