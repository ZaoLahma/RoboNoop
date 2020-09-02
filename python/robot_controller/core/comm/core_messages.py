from .message_base import MessageBase
from ..log.log import Log
import struct

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

ALL_CORE_MESSAGES = [HeartbeatReq, HeartbeatCfm]
