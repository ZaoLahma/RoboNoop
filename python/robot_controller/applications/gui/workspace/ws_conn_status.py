from ....core.log.log import Log
from ....core.comm.comm_utils import CommUtils
from ..comm.comm_ctxt import CommCtxt
from .core.workspace_base import WorkspaceBase

from tkinter import ttk
from tkinter import LEFT
from tkinter import Frame

class WsConnStatus(WorkspaceBase):
    def __init__(self, parent_frame, ws_controller, ws_resolution):
        WorkspaceBase.__init__(self, parent_frame, ws_controller, ws_resolution)
        self.Active = False
        self.applications = ["masterchief", "garrus", "daredevil", "fear", "kratos"]
        self.appl_labels = []

    def update_appl_labels(self):
        curr_index = 0
        for application in self.applications:
            appl_status = "{0} : {1}".format(application, CommUtils.is_connected(CommCtxt.get_comm_if(), application))
            self.appl_labels[curr_index].configure(text = appl_status)
            curr_index += 1

    @staticmethod
    def get_id():
        return "Start"

    def refresh(self):
        if self.active:
            self.after(500, self.refresh)
            self.update_appl_labels()

    def activate(self):
        Log.log("Activate called")
        self.ws_header = ttk.Label(self, text = "Connection status", anchor = "w", width = 20)
        self.ws_header.grid(row = 0, column = 0)
        for application in self.applications:
            appl_label = ttk.Label(self, text = "{0} : {1}".format(application, False), anchor = "w", width = 20)
            appl_label.grid(row = len(self.appl_labels) + 1, column = 0)
            self.appl_labels.append(appl_label)
        self.active = True
        self.after(500, self.refresh)

    def pause(self):
        Log.log("Pause called")
        self.active = False

    def deactivate(self):
        Log.log("Deactivate called")
        self.active = False
        self.appl_labels = []