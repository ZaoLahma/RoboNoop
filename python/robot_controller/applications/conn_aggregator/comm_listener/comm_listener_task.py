from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.comm.message_protocol import MessageProtocol
from ....core.state.state import State
from ....core.state.state import StateHandler
from ....core.comm.comm_utils import CommUtils
from ....core.config.config import Config

class CommListenerTask(TaskBase):
    def __init__(self, comm_aggregate_if, comm_if):
        self.comm_aggregate_if = comm_aggregate_if
        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_init, "CONNECT_START", "INIT"),
            State("CONNECT_START", self.handle_connect_start, "CONNECT_DAREDEVIL", "CONNECT_START"),
           # State("CONNECT_MASTERCHIEF", self.handle_masterchief, "CONNECT_DAREDEVIL", "CONNECT_START"),
            State("CONNECT_DAREDEVIL", self.handle_connect_daredevil, "ENABLED", "CONNECT_START"),
            #State("CONNECT_FEAR", self.handle_connect_fear, "CONNECT_KRATOS", "CONNECT_START"),
            #State("CONNECT_KRATOS", self.handle_connect_kratos, "ENABLED", "CONNECT_START"),
            State("ENABLED", self.handle_enabled, "ESCAPING", "INHIBITED")
        ]
        self.state_handler = StateHandler(self.state_def, "INIT")

    def run(self):
        func = self.state_handler.get_state_func()
        func()

    def handle_init(self):
        app_config = Config.get_config_val("application")
        port_no = app_config["comm"]["message_proxy"]["port-no"]
        self.comm_if.publish_service(port_no)
        self.state_handler.transition()

    def handle_connect_start(self):
        self.state_handler.transition()

    def handle_masterchief(self):
        fail = True != CommUtils.connect(self.comm_aggregate_if, "masterchief")
        self.state_handler.transition(fail)

    def handle_connect_daredevil(self):
        fail = True != CommUtils.connect(self.comm_aggregate_if, "daredevil")
        self.state_handler.transition(fail)

    def handle_connect_fear(self):
        fail = True != CommUtils.connect(self.comm_aggregate_if, "fear")
        self.state_handler.transition(fail)
    
    def handle_connect_kratos(self):
        fail = True != CommUtils.connect(self.comm_aggregate_if, "kratos")
        self.state_handler.transition(fail)

    def handle_enabled(self):
        messages = self.comm_aggregate_if.get_all_messages()
        for message in messages:
            Log.log("Message: " + str(message))
        self.comm_aggregate_if.invalidate_messages()