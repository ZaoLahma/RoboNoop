from ..runtime.task_base import TaskBase
from ..log.log import Log

from time import time

class MessageStorage(TaskBase):
    def __init__(self, comm_if):
        TaskBase.__init__(self)
        self.comm_if = comm_if
        self.received_messages = {}

    def run(self):
        received_messages = self.comm_if.get_all_messages()
        #Log.log("Received messages: " + str(received_messages))
        self.comm_if.invalidate_messages()

        for message in received_messages:
            self.received_messages[message.get_msg_id()] = message

    def get_message(self, msg_id):
        return self.received_messages.get(msg_id)
        


    