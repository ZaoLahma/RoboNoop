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
from ..util.coord import Coord
from .human_detector import HumanDetector
from .vision_messages import ObjectsMessage

import numpy as np

from time import time

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
                
                Log.log("DETECTION START")
                now = time()
                bodies = self.human_detector.detect_bodies(image_data)
                faces = self.human_detector.detect_faces(image_data)
                Log.log("DETECTION TOOK " + str(time() - now) + " SECONDS")

                trnsfrm_fun = Coord.image_to_cam_centre

                bodies = np.array([trnsfrm_fun(rect, resolution) for rect in bodies])
                faces = np.array([trnsfrm_fun(rect, resolution) for rect in faces])

                Log.log("Detected these humans: " + str(bodies) + " " + str(faces))

                objects_msg = ObjectsMessage(image_msg.frame_no, bodies)
                self.comm_if.send_message(objects_msg)
            else:
                Log.log("Wrong image mode - skipping detection")
                mode_select = ImageModeSelect(color_mode = MONOCHROME)
                self.comm_if.send_message(mode_select)

        self.state_handler.transition(fail) 