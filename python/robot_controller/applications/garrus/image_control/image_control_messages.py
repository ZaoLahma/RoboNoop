from ....core.comm.message_base import MessageBase
from ....core.log.log import Log
from binascii import crc32

COLOR      = 0
MONOCHROME = 1

class ImageData(MessageBase):
    def __init__(self, resolution = None, color_mode = None, image_data = None):
        MessageBase.__init__(self)
        Log.log("Image data created")
        self.resolution = resolution
        self.color_mode = color_mode
        self.image_data = image_data

    @staticmethod
    def get_msg_id():
        return 30

    # 5 bytes header:
    #  0..1 - res x
    #  2..4 - res y
    #  5 - color mode
    #  6..n - data
    def encode(self):
        Log.log("Encode called")
        to_send = bytearray()
        to_send.extend(self.resolution[0].to_bytes(length = 2, byteorder = "big"))
        to_send.extend(self.resolution[1].to_bytes(length = 2, byteorder = "big"))
        to_send.extend(self.color_mode.to_bytes(length = 1, byteorder = "big"))
        to_send.extend(self.image_data)
        Log.log("Endcode exit")
        return to_send

    def decode(self, data):
        res_x = int.from_bytes(data[0:2], byteorder = "big")
        res_y = int.from_bytes(data[2:4], byteorder = "big")
        self.resolution = (res_x, res_y)
        self.color_mode = data [4]
        self.image_data = data[5:]

class ImageModeSelect(MessageBase):
    def __init__(self, resolution = (640, 480), mode = COLOR):
        MessageBase.__init__(self)
        self.resolution = resolution
        self.mode = mode

    @staticmethod
    def get_msg_id():
        return 31
    
    def encode(self):
        return None

    def decode(self):
        pass

ALL_IMAGE_CONTROL_MESSAGES = [ImageData, ImageModeSelect]