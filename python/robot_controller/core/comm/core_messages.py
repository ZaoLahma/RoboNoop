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

class CapabilitiesInd(MessageBase):
    def __init__(self, capabilities = None):
        self.capabilities = capabilities

    @staticmethod
    def get_msg_id():
        return 3

    def encode(self):
        ret_val = None
        if None != self.capabilities:
            ret_val = bytes(self.capabilities)
        return ret_val

    def decode(self, data):
        self.capabilities = []
        for b in data:
            self.capabilities.append(b)

ALL_CORE_MESSAGES = [HeartbeatReq, HeartbeatCfm, CapabilitiesInd]
