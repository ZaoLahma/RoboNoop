from ....core.comm.message_base import MessageBase
from ....core.log.log import Log
import struct

class UnlockInd(MessageBase):
    @staticmethod
    def get_msg_id():
        return 100

    def encode(self):
        return None
    
    def decode(self, data):
        return None

class ReleaseCtrlInd(MessageBase):
    def __init__(self, sub_system=1000):
        self.sub_system = sub_system

    @staticmethod
    def get_msg_id():
        return 101

    def encode(self):
        data = struct.pack(">H", self.sub_system)
        return data
    
    def decode(self, data):
        self.sub_system = struct.unpack(">H", data[0:])[0]
        Log.log("sub_system {0}".format(self.sub_system))
 

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
        return 102

    def encode(self):
        data = struct.pack(">H", self.direction)
        data += struct.pack(">H", self.power)
        data += struct.pack(">H", self.sub_system)
        return data
    
    def decode(self, data):
        self.direction = struct.unpack(">H", data[0:2])[0]
        self.power = struct.unpack(">H", data[2:4])[0]
        self.sub_system = struct.unpack(">H", data[4:])[0]
        Log.log("direction {0}, power {1}, sub_system {2}".format(self.get_direction_string(self.direction), self.power, self.sub_system))

    def get_direction_string(self, direction):
        if MoveInd.STOP == direction:
            return "STOP"
        elif MoveInd.FORWARD == direction:
            return "FORWARD"
        elif MoveInd.LEFT == direction:
            return "LEFT"
        elif MoveInd.RIGHT == direction:
            return "RIGHT"
        elif MoveInd.BACKWARD == direction:
            return "BACKWARD"
        else:
            return "UNKNOWN"

ALL_MOTOR_CONTROL_MESSAGES = [ReleaseCtrlInd, MoveInd]