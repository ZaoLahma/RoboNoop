from ....core.log.log import Log
from ....core.comm.comm_utils import CommUtils
from ...garrus.image_control.image_control_messages import ImageData
from ...garrus.image_control.image_control_messages import ImageModeSelect
from ...garrus.image_control.image_control_messages import COLOR
from ...garrus.image_control.image_control_messages import MONOCHROME
from ...vision.task.vision_messages import ObjectsMessage
from ...vision.util.coord import Coord
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

class Frame:
    def __init__(self, frame_no, messages):
        self.frame_no = frame_no
        self.messages = messages

    def get_message(self, msg_id):
        ret_val = None
        for message in self.messages:
            if message.get_msg_id() == msg_id:
                ret_val = message
                break
        return ret_val

class FrameCtxt():
    def __init__(self):
        self.last_frame = None
        self.messages = []

    def garbage_collect(self, frame_no):
        messages = self.messages
        self.messages = []
        
        for message in messages:
            if message.frame_no > frame_no:
                self.messages.append(message)

    def construct_frame(self, message):
        for compare_message in self.messages:
            if message.get_msg_id() != compare_message.get_msg_id() and message.frame_no == compare_message.frame_no:
                #We have a complete frame
                if self.last_frame == None or message.frame_no > self.last_frame.frame_no:
                    self.last_frame = Frame(message.frame_no, [message, compare_message])
                    self.garbage_collect(message.frame_no)

    def handle_message(self, message):
        new_frame = True
        for msg in self.messages:
            if message.frame_no == msg.frame_no:
                new_frame = False
                break
        if True == new_frame:
            #Log.log("New frame message: " + str(message.frame_no))
            self.messages.append(message)
        self.construct_frame(message)

    def get_most_recent_complete_frame(self):
        return self.last_frame

class WsVision(WorkspaceBase):
    def __init__(self, parent_frame, ws_controller, ws_resolution):
        WorkspaceBase.__init__(self, parent_frame, ws_controller, ws_resolution)
        self.active = False
        self.rendering = False
        self.color_mode = MONOCHROME
        self.image_label = Label(self)
        self.image_label.pack(side = TOP)
        self.image = None

        self.frame_ctxt = FrameCtxt()

    @staticmethod
    def get_id():
        return "Vision"

    def refresh(self):
        #Log.log("refresh")
        if True == self.rendering:
            Log.log("Returning due to rendering")
            return
        if self.active and False == self.rendering:
            self.rendering = True
            msg = CommCtxt.get_comm_if().get_message(ImageData.get_msg_id())
            if None != msg:
                self.frame_ctxt.handle_message(msg)
            #Log.log("ImageData: " + str(msg))
            msg = CommCtxt.get_comm_if().get_message(ObjectsMessage.get_msg_id())
            if None != msg:
                self.frame_ctxt.handle_message(msg)
            #Log.log("ObjectsMessage: " + str(msg))
            frame = self.frame_ctxt.get_most_recent_complete_frame()
            if None != frame:
                #Log.log("Have frame " + str(frame.frame_no))
                image_msg = frame.get_message(ImageData.get_msg_id())
                objects_msg = frame.get_message(ObjectsMessage.get_msg_id())

                #for obj in objects_msg.objects:
                #    Log.log("Detected orig coords: " + str(obj) + " transformed: " + str(Coord.cam_centre_to_image(obj, image_msg.resolution)))

                self.show_image(image_msg, objects_msg)
            self.rendering = False
            self.after(200, self.refresh)

    def show_image(self, image_message, objects_message):
        to_show = None
        color_mode = image_message.color_mode
        resolution = image_message.resolution
        image = image_message.image_data
        objects = objects_message.objects
        if MONOCHROME == color_mode:
            to_show = np.frombuffer(image, dtype=np.uint8).reshape((resolution[1], resolution[0]))

            image_coord_objects = []
            for rect in objects:
                image_coord_objects.append(Coord.cam_centre_to_image(rect, resolution))

            image_coord_objects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in image_coord_objects])

            #Log.log("Objects: " + str(image_coord_objects))

            for (xA, yA, xB, yB) in image_coord_objects:
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