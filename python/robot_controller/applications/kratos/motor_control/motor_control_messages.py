from ....core.comm.message_base import MessageBase
from ....core.log.log import Log
import struct

class MoveInd(MessageBase):
    STOP     = 0
    FORWARD  = 1
    LEFT     = 2
    RIGHT    = 3
    BACKWARD = 4
    def __init__(self, direction=STOP, power=100, sub_system=1000):
        self.direction = direction
        self.power = power
        self.sub_system = sub_system

    @staticmethod
    def get_msg_id():
        return 100

    def encode(self):
        data = struct.pack(">H", self.direction)
        data += struct.pack(">H", self.power)
        return data
    
    def decode(self, data):
        self.direction = struct.unpack(">H", data[0:2])[0]
        self.power = struct.unpack(">H", data[2:])[0]
        Log.log("direction {0}, power {1}".format(self.direction, self.power))

ALL_MOTOR_CONTROL_MESSAGES = [MoveInd]