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
            self.comm_interface.connect("localhost", 3030)
            self.connected = True

        msg = self.comm_interface.get_message(AllCapabilities.get_msg_id())
        if None != msg:
            Log.log("Received msg " + str(msg.get_msg_id()))