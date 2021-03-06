from ..log.log import Log
from .message_base import MessageBase
import struct

class MessageProtocol:
    def __init__(self, message_classes):
        self.message_classes = message_classes

    @staticmethod
    def encode_message(message):
        data = struct.pack('<B', message.get_msg_id())
        payload = message.encode()

        if None != payload:
            data += payload

        return data

    def decode_message(self, data):
        msg_id = struct.unpack('<B', data[0:1])[0]
        msg = None
        for message_class in self.message_classes:
            if msg_id == message_class.get_msg_id():
                msg = message_class()
                break
        if None != msg:
            msg.decode(data[1:])
        return msg
