from ....core.comm.message_base import MessageBase
from ....core.log.log import Log
import struct

class SonarDataInd(MessageBase):
    def __init__(self, distance=-1):
        self.distance = distance

    @staticmethod
    def get_msg_id():
        return 20

    def encode(self):
        data = struct.pack(">H", self.distance)
        return data
    
    def decode(self, data):
        self.distance = struct.unpack(">H", data[0:2])[0]

ALL_SONAR_MESSAGES = [SonarDataInd]