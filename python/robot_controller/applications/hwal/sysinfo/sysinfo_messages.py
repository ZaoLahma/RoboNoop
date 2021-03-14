from ....core.comm.message_base import MessageBase

class SysinfoMessage(MessageBase):
    def __init__(self):
        MessageBase.__init__(self)

    def encode(self):
        return None

    def decode(self):
        return None