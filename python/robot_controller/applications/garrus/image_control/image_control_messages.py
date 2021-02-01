from ....core.comm.message_base import MessageBase
from ....core.log.log import Log
from binascii import crc32

class BinaryDataTransfer(MessageBase):
    def __init__(self, data_buf = None):
        self.data_buf = data_buf

    @staticmethod
    def get_msg_id():
        return 2
        
    def encode(self):
        Log.log("Encode CRC: {:#010x}".format(crc32(self.data_buf)))
        return self.data_buf

    def decode(self, data):
        self.data_buf = data
        Log.log("Decode CRC: {:#010x}".format(crc32(self.data_buf)))

ALL_IMAGE_CONTROL_MESSAGES = [BinaryDataTransfer]