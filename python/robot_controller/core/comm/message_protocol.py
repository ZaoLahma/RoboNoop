from ..log.log import Log
from .message_base import MessageBase
from time import time
import struct

class MessageProtocol:
    def __init__(self, message_classes):
        self.message_classes = message_classes

    @staticmethod
    def encode_message(message):
        now = time()
        data = struct.pack('>d', now)
        data += struct.pack('>B', message.get_msg_id())
        payload = message.encode()

        if None != payload:
            data += payload

        return data

    def decode_message(self, data):
        now = time()
        msg_time = struct.unpack('>d', data[0:8])[0]
        Log.log("Age when received: " + str(now - msg_time))

        if ((now - msg_time) > 1.0):
            Log.log("Throwing away message that is too old")
            return None

        msg_id = struct.unpack('>B', data[8:9])[0]
        msg = None
        for message_class in self.message_classes:
            if msg_id == message_class.get_msg_id():
                msg = message_class()
                break
        if None != msg:
            msg.msg_receive_time = time()
            msg.msg_send_time = msg_time
            msg.decode(data[9:])
        return msg
