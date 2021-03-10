from time import time

class MessageBase:
    def __init__(self):
        self.msg_create_time = time()
        self.msg_receive_time = None
        self.msg_send_time = None

    @staticmethod
    def get_msg_id(self):
        raise NotImplementedError

    def encode(self):
        raise NotImplementedError

    def decode(self, data):
        raise NotImplementedError