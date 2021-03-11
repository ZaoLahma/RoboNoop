from ....core.log.log import Log
from ....core.comm.comm_utils import CommUtils
from ....applications.garrus.image_control.image_control_messages import ImageData
from ...garrus.image_control.image_control_messages import COLOR
from ...garrus.image_control.image_control_messages import MONOCHROME
from ..comm.comm_ctxt import CommCtxt
from .core.workspace_base import WorkspaceBase

from tkinter import ttk
from tkinter import Canvas
from tkinter import TOP
from tkinter import PhotoImage
from tkinter import Label

from PIL import Image
from PIL import ImageTk

from time import time

import numpy as np

import cv2

class WsImage(WorkspaceBase):
    def __init__(self, parent_frame, ws_controller, ws_resolution):
        WorkspaceBase.__init__(self, parent_frame, ws_controller, ws_resolution)
        self.active = False
        self.rendering = False
        self.image_label = Label(self)
        self.image_label.pack(side = TOP)
        self.image = None
        self.hex_row_buffer = []
        self.hex_row_buffer_size = 0

    @staticmethod
    def get_id():
        return "Image"

    def refresh(self):
        if True == self.rendering:
            Log.log("Returning due to rendering")
            return
        if self.active and False == self.rendering:
            self.rendering = True
            msg = CommCtxt.get_comm_if().get_message(ImageData.get_msg_id())
            if None != msg:
                now = time()
                Log.log("Age from creation to sending: " + str(msg.msg_send_time - msg.msg_create_time))
                Log.log("Age from sending to now: " + str(now - msg.msg_send_time))
                Log.log("Age from receiving to now: " + str(now - msg.msg_receive_time))
                Log.log("Total age: " + str(now - msg.msg_create_time))
                self.show_image(msg.resolution, msg.color_mode, msg.image_data)
            self.rendering = False
            self.after(100, self.refresh)

    def show_image(self, resolution, color_mode, image):
        #Log.log("enter show_image")
        to_show = np.frombuffer(image, dtype=np.uint8).reshape((resolution[1], resolution[0], 3))
        to_show = Image.fromarray(to_show)
        self.image = ImageTk.PhotoImage(to_show)
        self.image_label.configure(image=self.image)
        #Log.log("exit show_image")

    def activate(self):
        self.active = True
        self.after(0, self.refresh)

    def deactivate(self):
        self.active = False
        while self.rendering:
            Log.log("Waiting...")