from ....core.comm.message_base import MessageBase

from json import dumps
from json import loads

class SysinfoMessage(MessageBase):
    def __init__(self):
        MessageBase.__init__(self)
        self.sysinfo = {}

    @staticmethod
    def get_msg_id():
        return 50

    def add_sysinfo(self, sysinfo, value):
        self.sysinfo[sysinfo] = value

    def encode(self):
        return dumps(self.sysinfo).encode()

    def decode(self, data):
        self.hw_info = loads(data.decode())

ALL_SYSINFO_MESSAGES = [SysinfoMessage]