from .message_base import MessageBase
from ..log.log import Log
import struct
import json

class HeartbeatReq(MessageBase):
    @staticmethod
    def get_msg_id():
        return 0

    def encode(self):
        return None
    
    def decode(self, data):
        return None

class HeartbeatCfm(MessageBase):
    @staticmethod
    def get_msg_id():
        return 1

    def encode(self):
        return None

    def decode(self, data):
        return None

class DataTransfer(MessageBase):
    def __init__(self):
        self.data = {}

    def add_data(self, data_type, data):
        try:
            dtype = self.data[data_type]
        except KeyError:
            self.data[data_type] = []
            dtype = self.data[data_type]
        dtype.append(data)

    def get_data(self, data_type):
        return self.data[data_type]

    @staticmethod
    def get_msg_id():
        return 2
        
    def encode(self):
        return json.dumps(self.data).encode("utf-8")

    def decode(self, data):
        json.loads(data.decode("utf-8"))

ALL_CORE_MESSAGES = [HeartbeatReq, HeartbeatCfm, DataTransfer]
