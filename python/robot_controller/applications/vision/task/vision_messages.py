from ....core.comm.message_base import MessageBase
from ....core.log.log import Log
from ..util.coord import Coord
from ..util.coord import Coord

import struct
import math

class ObjectsMessage(MessageBase):
    PACK_FACTOR = 100 # To be able to send the two decimal floats as one byte objects
    def __init__(self, frame_no = 0, objects = None):
        MessageBase.__init__(self)
        self.frame_no = frame_no
        self.objects = objects
        Log.log("INIT OBJECTS MESSAGE")

    @staticmethod
    def get_msg_id():
        return 40

    def encode(self):
        Log.log("ENCODE OBJECTS MESSAGE")
        data = struct.pack('>I', self.frame_no)
        data += struct.pack('>B', len(self.objects))

        for rect in self.objects:
            Log.log("packing: " + str(rect[0] * ObjectsMessage.PACK_FACTOR))
            data += struct.pack('>B', math.floor((rect[0] - Coord.X_OFFSET) * ObjectsMessage.PACK_FACTOR))
            data += struct.pack('>B', math.floor((rect[1] - Coord.Y_OFFSET) * ObjectsMessage.PACK_FACTOR))
            data += struct.pack('>B', math.floor((rect[2] - Coord.X_OFFSET) * ObjectsMessage.PACK_FACTOR))
            data += struct.pack('>B', math.floor((rect[3] - Coord.Y_OFFSET) * ObjectsMessage.PACK_FACTOR))

        Log.log("Encode returning " + str(data))

        return data

    def decode(self, data):
        Log.log("DECODE OBJECTS MESSAGE")
        if None == self.objects:
            self.objects = []
        self.frame_no = int.from_bytes(data[0:4], byteorder = 'big')
        num_rects = data[4]

        for i in range(num_rects):
            Log.log("i: " + str(i))
            x = data[5 + i]
            y = data[6 + i]
            w = data[7 + i]
            h = data[8 + i]
            rect = [(x / ObjectsMessage.PACK_FACTOR) + Coord.X_OFFSET, (y / ObjectsMessage.PACK_FACTOR) + Coord.Y_OFFSET, (w / ObjectsMessage.PACK_FACTOR) + Coord.X_OFFSET, (h / ObjectsMessage.PACK_FACTOR) + Coord.Y_OFFSET]
            self.objects.append(rect)
        Log.log("frame_no objects: " + str(self.frame_no))

ALL_VISION_MESSAGES = [ObjectsMessage]