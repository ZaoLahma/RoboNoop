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

class WsImage(WorkspaceBase):
    def __init__(self, parent_frame, ws_controller, ws_resolution):
        WorkspaceBase.__init__(self, parent_frame, ws_controller, ws_resolution)
        self.active = False
        self.rendering = False
        self.canvas = Canvas(self, width=self.ws_resolution[0], height=self.ws_resolution[1], bg="#000000")
        self.canvas.pack(side = TOP)
        self.image = PhotoImage(width=self.ws_resolution[0], height=self.ws_resolution[1])
        self.canvas.create_image((self.ws_resolution[0]/2, self.ws_resolution[1]/2), image=self.image, state="normal")
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
                self.show_image(msg.resolution, msg.color_mode, msg.image_data)
            self.rendering = False
            self.after(100, self.refresh)

    def show_image(self, resolution, color_mode, image):
        Log.log("Show image begin")
        self.rendering = True
        x = 0
        y = 0
        pixel_val = None

        if COLOR == color_mode:
            pixel_val = [0, 0, 0]
        elif MONOCHROME == color_mode:
            pixel_val = [0]
        else:
            raise NotImplementedError

        hex_image = []
        hex_row = []
        hex_row.append('{')
        for i in range(0, len(image), len(pixel_val)):
            hex_row.append("#")
            for o in range(0, len(pixel_val)):
                hex_row.append("%02x" % image[i + o])
            hex_row.append(" ")
            x += 1
            if x == resolution[0]:
                hex_row.append('}')
                hex_image.append(''.join(hex_row))
                hex_row = []
                hex_row.append(' {')
                x = 0
                y += 1
        if self.active and not self.image == None:
            Log.log("Before put")
            self.image.put(''.join(hex_image), to=(0, 0, resolution[0], resolution[1]))
            Log.log("After put")
        Log.log("Show image end")

    def activate(self):
        self.active = True
        self.after(0, self.refresh)

    def deactivate(self):
        self.active = False
        while self.rendering:
            Log.log("Waiting...")