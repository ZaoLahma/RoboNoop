from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.comm.core_messages import DataTransfer
from ....core.config.config import Config
from io import BytesIO
from base64 import b64encode

try:
    import picamera
except ImportError:
    from . import rpi_camera_stub as picamera

class ImageControlTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if
        self.camera = picamera.PiCamera()

        application_config = Config.get_config_val("application")
        resolution_x = application_config["vision"]["garrus"]["image_x_res"]
        resolution_y = application_config["vision"]["garrus"]["image_y_res"]

        self.camera.resolution = (resolution_x, resolution_y)


    def run(self):
        Log.log("Run")
        image = BytesIO()
        self.camera.capture(image, "rgb", use_video_port=True)
        image = bytearray(image.getvalue())
        image_data = b64encode(image).decode('utf-8')

        data_transfer = DataTransfer()
        data_transfer.add_data("image_data", image_data)
        self.comm_if.send_message(data_transfer)


