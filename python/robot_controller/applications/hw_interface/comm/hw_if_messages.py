from ....core.comm.message_base import MessageBase

from json import dumps
from json import loads

class DataTransferMessage(MessageBase):
    def __init__(self):
        MessageBase.__init__(self)
        self.data = {}

    @staticmethod
    def get_msg_id():
        return 50

    def add_data(self, data_id, value):
        self.data[data_id] = value

    def encode(self):
        return dumps(self.data).encode()

    def decode(self, data):
        self.data = loads(data.decode())

ALL_COMMAND_MESSAGES = [DataTransferMessage]