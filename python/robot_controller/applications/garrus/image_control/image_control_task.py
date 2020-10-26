from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.comm.core_messages import BinaryDataTransfer
from ....core.config.config import Config
from ....core.comm.comm_utils import CommUtils
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

        CommUtils.publish_service(self.comm_if, "garrus")


    def run(self):
        Log.log("======= Run ======")
        image = BytesIO()
        self.camera.capture(image, "rgb", use_video_port=True)
        image = bytearray(image.getvalue())
        
        data_transfer = BinaryDataTransfer(image)
        self.comm_if.send_message(data_transfer)


