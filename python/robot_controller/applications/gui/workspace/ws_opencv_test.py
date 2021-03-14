from ....core.log.log import Log
from ....core.comm.comm_utils import CommUtils
from ....applications.garrus.image_control.image_control_messages import ImageData
from ....applications.garrus.image_control.image_control_messages import ImageModeSelect
from ...garrus.image_control.image_control_messages import COLOR
from ...garrus.image_control.image_control_messages import MONOCHROME
from ..comm.comm_ctxt import CommCtxt
from .core.workspace_base import WorkspaceBase

from tkinter import ttk
from tkinter import Canvas
from tkinter import TOP
from tkinter import BOTTOM
from tkinter import PhotoImage
from tkinter import Label

from PIL import Image
from PIL import ImageTk

from time import time

import numpy as np

import cv2

class WsOpenCVTest(WorkspaceBase):
    def __init__(self, parent_frame, ws_controller, ws_resolution):
        WorkspaceBase.__init__(self, parent_frame, ws_controller, ws_resolution)
        self.active = False
        self.rendering = False
        self.color_mode = MONOCHROME
        self.image_label = Label(self)
        self.image_label.pack(side = TOP)
        self.image = None
        self.opencv_state_toggle = ttk.Button(self, text = "OpenCV Enable", command = lambda : self.toggle_opencv())
        self.opencv_state_toggle.pack(side = BOTTOM)
        self.hex_row_buffer = []
        self.hex_row_buffer_size = 0
        self.opencv_state = "off"
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        msg = ImageModeSelect(color_mode=self.color_mode)
        CommCtxt.get_comm_if().send_message(msg)

    @staticmethod
    def get_id():
        return "OpenCV"

    def toggle_opencv(self):
        if "off" == self.opencv_state:
            self.opencv_state_toggle.configure(text = "OpenCV Disable")
            self.opencv_state = "on"
        else:
            self.opencv_state_toggle.configure(text = "OpenCV Enable")
            self.opencv_state = "off"

    def detect_objects(self, image):
        rects = []
        if "on" == self.opencv_state:
            (rects, weights) = self.hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
            #(rects, weights) = self.hog.detectMultiScale(image, winStride=(8, 8))
        return rects

    def refresh(self):
        if True == self.rendering:
            Log.log("Returning due to rendering")
            return
        if self.active and False == self.rendering:
            self.rendering = True
            msg = CommCtxt.get_comm_if().get_message(ImageData.get_msg_id())
            if None != msg:
                self.show_image(msg.resolution, msg.color_mode, msg.image_data)
            self.rendering = False
            self.after(200, self.refresh)

    def show_image(self, resolution, color_mode, image):
        to_show = None
        if MONOCHROME == color_mode:
            to_show = np.frombuffer(image, dtype=np.uint8).reshape((resolution[1], resolution[0]))
            rects = self.detect_objects(to_show)
            rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])

            for (xA, yA, xB, yB) in rects:
                cv2.rectangle(to_show, (xA, yA), (xB, yB), (0), 2)

            to_show = Image.fromarray(to_show)
            self.image = ImageTk.PhotoImage(to_show)
            self.image_label.configure(image=self.image)

    def activate(self):
        self.active = True
        self.after(0, self.refresh)

    def deactivate(self):
        self.active = False
        while self.rendering:
            Log.log("Waiting...")
        msg = ImageModeSelect(color_mode=COLOR)
        CommCtxt.get_comm_if().send_message(msg)