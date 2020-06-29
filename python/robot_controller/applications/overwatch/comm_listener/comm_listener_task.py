from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.comm.message_protocol import MessageProtocol
from ....core.comm.core_messages import AllCapabilities
from ....core.comm.core_messages import CapabilitiesReq
from ....core.comm.core_messages import CapabilitiesCfm

class CommListenerTask(TaskBase):
    def __init__(self, comm_interface):
        self.comm_interface = comm_interface
        self.connected = False

    def run(self):
        if False == self.connected:
            try:
                self.comm_interface.connect("localhost", 3030)
                self.connected = True
            except Exception as e:
                Log.log("Connection failed: " + str(e))

        msgs = self.comm_interface.get_all_messages()
        if None != msgs:
            for msg in msgs:
                Log.log("Received msg " + str(msg.get_msg_id()))