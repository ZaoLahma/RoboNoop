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

ALL_CORE_MESSAGES = [HeartbeatReq, HeartbeatCfm, BinaryDataTransfer]
