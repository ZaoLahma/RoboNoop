from ....core.log.log import Log
from ....core.comm.comm_utils import CommUtils
from ..comm.comm_ctxt import CommCtxt
from .core.workspace_base import WorkspaceBase

from tkinter import ttk

class WsConnStatus(WorkspaceBase):
    def __init__(self, parent_frame, ws_controller):
        WorkspaceBase.__init__(self, parent_frame, ws_controller)
        self.ws_header = None
        self.ws_content = None
        self.Active = False

    def get_conn_status_string(self):
        ret_val = "masterchief : {0}".format(CommUtils.is_connected(CommCtxt.get_comm_if(), "masterchief"))
        ret_val +="\ngarrus: {0}".format(CommUtils.is_connected(CommCtxt.get_comm_if(), "garrus"))
        ret_val +="\ndaredevil: {0}".format(CommUtils.is_connected(CommCtxt.get_comm_if(), "daredevil"))
        ret_val +="\nfear: {0}".format(CommUtils.is_connected(CommCtxt.get_comm_if(), "fear"))
        ret_val +="\nkratos: {0}".format(CommUtils.is_connected(CommCtxt.get_comm_if(), "kratos"))
        return ret_val

    @staticmethod
    def get_id():
        return "Start"

    def refresh(self):
        if self.active:
            self.after(500, self.refresh)
            self.ws_content.configure(text = self.get_conn_status_string())

    def activate(self):
        Log.log("Activate called")
        self.ws_header = ttk.Label(self, text = "Connection status")
        self.ws_header.grid(row = 0, column = 0)
        self.ws_content = ttk.Label(self, text = "")
        self.ws_content.grid(row = 1, column = 0)
        self.active = True
        self.after(500, self.refresh)

    def pause(self):
        Log.log("Pause called")
        self.active = False

    def deactivate(self):
        Log.log("Deactivate called")
        self.ws_header.destroy()
        self.ws_content.destroy()
        self.active = False

    def destroy(self):
        Log.log("Destroy called")
        self.active = False