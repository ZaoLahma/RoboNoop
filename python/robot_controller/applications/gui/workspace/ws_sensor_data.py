from ....core.log.log import Log
from .core.workspace_base import WorkspaceBase

from tkinter import ttk

class WsSensorData(WorkspaceBase):
    def __init__(self, parent_frame, ws_controller):
        WorkspaceBase.__init__(self, parent_frame, ws_controller)
        self.ws_header = None
        self.Active = False

    @staticmethod
    def get_id():
        return "Sensor"

    def refresh(self):
        if self.active:
            self.after(500, self.refresh)

    def activate(self):
        Log.log("Activate called")
        self.ws_header = ttk.Label(self, text = "Sensor data")
        self.ws_header.grid(row = 0, column = 0)
        self.active = True
        self.after(500, self.refresh)

    def pause(self):
        Log.log("Pause called")
        self.active = False

    def deactivate(self):
        Log.log("Deactivate called")
        self.ws_header.destroy()
        self.active = False

    def destroy(self):
        Log.log("Destroy called")
        self.active = False