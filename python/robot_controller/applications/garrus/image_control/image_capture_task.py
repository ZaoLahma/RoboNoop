from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.config.config import Config
from ....core.comm.comm_utils import CommUtils
from .image_control_messages import ImageData
from .image_control_messages import ImageModeSelect
from .image_control_messages import COLOR
from .image_control_messages import MONOCHROME
from io import BytesIO

import numpy as np

from time import time

try:
    import picamera
except ImportError:
    from . import rpi_camera_stub as picamera

class ImageCaptureTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if
        self.color_mode = COLOR
        self.camera = picamera.PiCamera()
        self.camera.rotation = 180

        application_config = Config.get_config_val("application")
        resolution_x = application_config["vision"]["garrus"]["image_x_res"]
        resolution_y = application_config["vision"]["garrus"]["image_y_res"]

        self.resolution = (resolution_x, resolution_y)

        self.camera.resolution = self.resolution

        CommUtils.publish_service(self.comm_if, "garrus")

    def set_image_mode(self, resolution, color_mode):
        self.camera.resolution = resolution
        self.color_mode = color_mode

    def process_image(self, image):
        Log.log("Color mode: " + str(self.color_mode))
        if COLOR == self.color_mode:
            return bytearray(image.getvalue())
        image_data = bytearray()
        image_bytes = image.getvalue()
        Log.log("Will iterate over " + str(len(image_bytes)) + " bytes")
        for i in range(0, len(image_bytes), 3):
            pixel_val = int(((image_bytes[i] + image_bytes[i + 1] + image_bytes[i + 2]) / 3) + 0.5)
            image_data.append(pixel_val)
        Log.log("Iterate done")
        return image_data

    def process_image_new(self, image):
        if COLOR == self.color_mode:
            return bytearray(image.getvalue())
        image = image.getvalue()
        image = [int((sum(image[i : i + 3]) / 3) + 0.5) for i in range(0, len(image), 3)]
        Log.log("image size: " + str(len(image)))
        return bytearray(image)

    def process_image_numpy(self, image):
        now = time()
        image = bytearray(image.getvalue())
        if MONOCHROME == self.color_mode:
            image = bytearray(((np.frombuffer(image, dtype=np.uint8).reshape(len(image) // 3, 3).sum(axis = 1)) // 3).tolist())
        
        Log.log("Image processing took: " + str(time() - now) + " seconds")
        return image

    def process_image_numpy_new(self, image):
        now = time()
        image = bytearray(image.getvalue())
        if MONOCHROME == self.color_mode:
            image = bytearray(np.frombuffer(image, dtype=np.uint8, count=self.resolution[0] * self.resolution[1]).tolist())
        Log.log("Image processing took: " + str(time() - now) + " seconds")
        return image

    def run(self):
        msg = self.comm_if.get_message(ImageModeSelect.get_msg_id())
        if None != msg:
            self.set_image_mode(msg.resolution, msg.color_mode)
        Log.log("msg: " + str(msg))

        image = BytesIO()
        format_str = "rgb"
        if MONOCHROME == self.color_mode:
            format_str = "yuv"

        self.camera.capture(image, format_str, use_video_port=False)
        image = self.process_image_numpy_new(image)
        Log.log("Captured image of size: " + str(len(image)))
        
        data_transfer = ImageData(self.resolution, self.color_mode, image)
        #Log.log("Before send message")
        self.comm_if.send_message(data_transfer)
        #Log.log("After send message")


