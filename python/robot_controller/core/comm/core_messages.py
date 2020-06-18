from .message_base import MessageBase
from ..log.log import Log
import struct

class AllCapabilities(MessageBase):
    @staticmethod
    def get_msg_id():
        return 65535

class CapabilitiesReq(MessageBase):
    @staticmethod
    def get_msg_id():
        return 0

    def encode(self):
        return None
    
    def decode(self, data):
        return None

class CapabilitiesCfm(MessageBase):
    def __init__(self, protocols = []):
        self.msg_ids = []
        for protocol in protocols:
            for message_class in protocol.message_classes:
                self.msg_ids.append(message_class.get_msg_id())

    @staticmethod
    def get_msg_id():
        return 1

    def encode(self):
        data = struct.pack(">H", len(self.msg_ids)) + struct.pack(">{}H".format(len(self.msg_ids)), *self.msg_ids)
        Log.log("CapabilitiesCfm encoded data " + str(data))
        return data

    def decode(self, data):
        size = struct.unpack(">H", data[0:2])[0]
        decoded = struct.unpack(">{}H".format(size), data[2:])

        for msg_id in decoded:
            self.msg_ids.append(msg_id)

        Log.log("CapabilitiesCfm decoded data " + str(self.msg_ids))

ALL_CORE_MESSAGES = [AllCapabilities, CapabilitiesReq, CapabilitiesCfm]
