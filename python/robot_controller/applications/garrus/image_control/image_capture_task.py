from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.config.config import Config
from ....core.comm.comm_utils import CommUtils
from .image_control_messages import ImageData
from .image_control_messages import COLOR
from .image_control_messages import MONOCHROME
from io import BytesIO

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

    def run(self):
        image = BytesIO()
        self.camera.capture(image, "rgb", use_video_port=False)
        image = bytearray(image.getvalue())
        Log.log("Captured image of size: " + str(len(image)))
        
        data_transfer = ImageData(self.resolution, self.color_mode, image)
        data_transfer.msg_create_time = time()
        self.comm_if.send_message(data_transfer)


