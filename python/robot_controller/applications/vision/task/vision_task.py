from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.state.state import State
from ....core.state.state import StateHandler
from ....core.comm.comm_utils import CommUtils
from ....core.config.config import Config
from ...garrus.image_control.image_control_messages import ImageData
from ...garrus.image_control.image_control_messages import COLOR
from ...garrus.image_control.image_control_messages import MONOCHROME
from ...garrus.image_control.image_control_messages import ImageModeSelect
from .human_detector import HumanDetector

import numpy as np

import time

class VisionTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if

        self.human_detector = HumanDetector()

        self.state_def =  [
            State("INIT", self.handle_init, "CONNECT_GARRUS", "INIT"),
            State("CONNECT_GARRUS", self.handle_connect_garrus, "ENABLED", "CONECT_GARRUS"),
            State("ENABLED", self.handle_enabled, "ENABLED", "CONNECT_GARRUS")
        ]
        self.state_handler = StateHandler(self.state_def, "INIT")

    def run(self):
        func = self.state_handler.get_state_func()
        func()

    def handle_init(self):
        app_config = Config.get_config_val("application")
        port_no = app_config["comm"]["vision"]["port-no"]
        self.comm_if.publish_service(port_no)
        self.state_handler.transition()

    def handle_connect_garrus(self):
        fail = True != CommUtils.connect(self.comm_if, "garrus")
        self.state_handler.transition(fail)

    def handle_enabled(self):
        fail = False == CommUtils.is_connected(self.comm_if, "garrus")

        image_msg = self.comm_if.get_message(ImageData.get_msg_id())
        if None != image_msg:
            if MONOCHROME == image_msg.color_mode:
                resolution = image_msg.resolution
                image_data = image_msg.image_data
                image_data = np.frombuffer(image_data, dtype=np.uint8).reshape((resolution[1], resolution[0]))
                humans = self.human_detector.detect_humans(image_data)
                Log.log("Detected these humans: " + str(humans))
            else:
                mode_select = ImageModeSelect(color_mode = MONOCHROME)
                self.comm_if.send_message(mode_select)

        self.state_handler.transition(fail)