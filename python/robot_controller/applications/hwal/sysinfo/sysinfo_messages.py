from ....core.comm.message_base import MessageBase

class SysinfoMessage(MessageBase):
    def __init__(self, hw_info = ""):
        MessageBase.__init__(self)
        self.hw_info = hw_info

    @staticmethod
    def get_msg_id():
        return 50

    def encode(self):
        return self.hw_info.encode()

    def decode(self, data):
        self.hw_info = data.decode()

ALL_SYSINFO_MESSAGES = [SysinfoMessage]