from ....core.log.log import Log
from ....core.comm.comm_utils import CommUtils
from ....applications.garrus.image_control.image_control_messages import ImageData
from ..comm.comm_ctxt import CommCtxt
from .core.workspace_base import WorkspaceBase

from tkinter import ttk
from tkinter import Canvas
from tkinter import TOP
from tkinter import PhotoImage

class WsImage(WorkspaceBase):
    def __init__(self, parent_frame, ws_controller, ws_resolution):
        WorkspaceBase.__init__(self, parent_frame, ws_controller, ws_resolution)
        self.active = False
        self.rendering = False
        self.canvas = Canvas(self, width=self.ws_resolution[0], height=self.ws_resolution[1], bg="#000000")
        self.canvas.pack(side = TOP)
        self.image = PhotoImage(width=self.ws_resolution[0], height=self.ws_resolution[1])
        self.canvas.create_image((self.ws_resolution[0]/2, self.ws_resolution[1]/2), image=self.image, state="normal")

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
                Log.log("Calling show_image")
                self.show_image(msg.data_buf)
            self.rendering = False
            self.after(100, self.refresh)

    def show_image(self, image):
        self.rendering = True
        byte_offset = 0
        x = 0
        y = 0
        R = 0
        G = 0
        B = 0
        hex_image = []
        hex_row = []
        hex_row.append('{')
        for byte in image:
            if 0 == byte_offset:
                R = byte
            elif 1 == byte_offset:
                G = byte
            elif 2 == byte_offset:
                B = byte
            byte_offset += 1
            if 3 == byte_offset:
                byte_offset = 0
                hex_row.append("#%02x%02x%02x " % (R, G, B))
                x += 1
                if x == self.ws_resolution[0]:
                    hex_row.append('}')
                    hex_image.append(''.join(hex_row))
                    hex_row = []
                    hex_row.append(' {')
                    x = 0
                    y += 1
        if self.active and not self.image == None:
            self.image.put(''.join(hex_image), to=(0, 0, self.ws_resolution[0], self.ws_resolution[1]))

    def activate(self):
        self.active = True
        self.after(0, self.refresh)

    def deactivate(self):
        self.active = False
        while self.rendering:
            Log.log("Waiting...")