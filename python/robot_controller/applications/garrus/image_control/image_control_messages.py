from ....core.comm.message_base import MessageBase

class BinaryDataTransfer(MessageBase):
    def __init__(self, data_buf = None):
        self.data_buf = data_buf

    @staticmethod
    def get_msg_id():
        return 2
        
    def encode(self):
        return self.data_buf

    def decode(self, data):
        self.data_buf = data