from .core.workspace_base import WorkspaceBase
from ....core.log.log import Log
from tkinter import ttk

class WsStart(WorkspaceBase):
    def __init__(self, parent_frame, ws_controller):
        Log.log("WsStart init called")
        WorkspaceBase.__init__(self, parent_frame, ws_controller)
        ws_header = ttk.Label(self, text = "This is the start workspace")
        ws_header.grid(row = 0, column = 0)

    @staticmethod
    def get_id():
        return "Start"

    def activate(self):
        Log.log("Activate called")

    def pause(self):
        Log.log("Pause called")

    def deactivate(self):
        Log.log("Deactivate called")

    def destroy(self):
        Log.log("Destroy called")