from ....core.comm.message_base import MessageBase
from ....core.log.log import Log
import struct

class RunMotorReq(MessageBase):
    def __init__(self, motor_id=-1, power=-1):
        self.motor_id = motor_id
        self.power = power

    @staticmethod
    def get_msg_id():
        return 100

    def encode(self):
        data = struct.pack(">H", self.motor_id)
        data += struct.pack(">H", self.power)
        return data
    
    def decode(self, data):
        self.motor_id = struct.unpack(">H", data[0:2])[0]
        self.power = struct.unpack(">H", data[2:])
        Log.log("motor_id {0}, power {1}".format(self.motor_id, self.power))

class RunMotorCfm(MessageBase):
    @staticmethod
    def get_msg_id():
        return 101

    def encode(self):
        return None
    
    def decode(self, data):
        return None

ALL_MOTOR_CONTROL_MESSAGES = [RunMotorReq, RunMotorCfm]