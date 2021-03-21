from ....core.comm.message_base import MessageBase
from ....core.log.log import Log
from binascii import crc32

COLOR      = 0
MONOCHROME = 1

class ImageData(MessageBase):
    def __init__(self, frame_no = 0, resolution = None, color_mode = None, image_data = None):
        MessageBase.__init__(self)
        #Log.log("Image data enter CTOR")
        self.frame_no = frame_no
        self.resolution = resolution
        self.color_mode = color_mode
        self.image_data = image_data
        #Log.log("Exit CTOR")

    @staticmethod
    def get_msg_id():
        return 30

    # 9 bytes header:
    #  0..3   frame_no
    #  4..5 - res x
    #  6..8 - res y
    #  8 - color mode
    #  6..n - data
    def encode(self):
        #Log.log("Encode called")
        to_send = bytearray()
        to_send.extend(self.frame_no.to_bytes(length=4, byteorder="big"))
        to_send.extend(self.resolution[0].to_bytes(length = 2, byteorder = "big"))
        to_send.extend(self.resolution[1].to_bytes(length = 2, byteorder = "big"))
        to_send.extend(self.color_mode.to_bytes(length = 1, byteorder = "big"))
        to_send.extend(self.image_data)
        #Log.log("Encode exit")
        return to_send

    def decode(self, data):
        self.frame_no = int.from_bytes(data[0:4], byteorder = "big")
        res_x = int.from_bytes(data[4:6], byteorder = "big")
        res_y = int.from_bytes(data[6:8], byteorder = "big")
        self.resolution = (res_x, res_y)
        self.color_mode = data[8]
        self.image_data = data[9:]
        #Log.log("Frame no: " + str(self.frame_no))

class ImageModeSelect(MessageBase):
    def __init__(self, resolution = (640, 480), color_mode = COLOR):
        MessageBase.__init__(self)
        self.resolution = resolution
        self.color_mode = color_mode

    @staticmethod
    def get_msg_id():
        return 31
    
    def encode(self):
        to_send = bytearray()
        to_send.extend(self.resolution[0].to_bytes(length = 2, byteorder = "big"))
        to_send.extend(self.resolution[1].to_bytes(length = 2, byteorder = "big"))
        to_send.extend(self.color_mode.to_bytes(length = 1, byteorder = "big"))
        return to_send

    def decode(self, data):
        Log.log("Decode enter")
        res_x = int.from_bytes(data[0:2], byteorder = "big")
        res_y = int.from_bytes(data[2:4], byteorder = "big")
        self.resolution = (res_x, res_y)
        self.color_mode = data[4]
        Log.log("Decode exit")

ALL_IMAGE_CONTROL_MESSAGES = [ImageData, ImageModeSelect]