from ....core.log.log import Log
from ....core.comm.comm_utils import CommUtils
from ..comm.comm_ctxt import CommCtxt
from .core.workspace_base import WorkspaceBase

from tkinter import ttk

class WsSensorData(WorkspaceBase):
    def __init__(self, parent_frame, ws_controller, ws_resolution):
        WorkspaceBase.__init__(self, parent_frame, ws_controller, ws_resolution)
        self.Active = False

    @staticmethod
    def get_id():
        return "Sensor data"

    def refresh(self):
        if self.active:
            self.ws_frame.after(500, self.refresh)

    def activate(self):
        Log.log("Activate called")
        self.ws_header = ttk.Label(self.ws_frame, text = "Sensor data", anchor = "nw", width = 20)
        self.ws_header.grid(row = 0 , column = 0)
        self.ws_test = ttk.Label(self.ws_frame, text = "Is this working?!\nTest\nTest", anchor = "nw", width = 20)
        self.ws_test.grid(row = 1, column = 0)
        self.active = True
        self.ws_frame.after(500, self.refresh)

    def pause(self):
        Log.log("Pause called")
        self.active = False

    def deactivate(self):
        Log.log("Deactivate called")
        WorkspaceBase.destroy(self)
        self.active = False