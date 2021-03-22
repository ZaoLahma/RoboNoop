from ....core.log.log import Log
from ....core.comm.comm_utils import CommUtils
from ...daredevil.sonar_control.sonar_control_messages import SonarDataInd
from ...hwal.sysinfo.sysinfo_messages import SysinfoMessage
from ..comm.comm_ctxt import CommCtxt
from .core.workspace_base import WorkspaceBase

from tkinter import ttk
from time import time

class WsSensorData(WorkspaceBase):
    def __init__(self, parent_frame, ws_controller, ws_resolution):
        WorkspaceBase.__init__(self, parent_frame, ws_controller, ws_resolution)
        self.Active = False

    @staticmethod
    def get_id():
        return "Sensor data"

    def refresh(self):
        if self.active:
            label_text = ""
            sonar_msg = CommCtxt.get_comm_if().get_message(SonarDataInd.get_msg_id())
            if None != sonar_msg:
                Log.log("sonar_msg age: " + str(time() - sonar_msg.msg_send_time))
                distance = sonar_msg.distance
                label_text += "Distance: {0}".format(distance)

            sysinfo_msg = CommCtxt.get_comm_if().get_message(SysinfoMessage.get_msg_id())
            if None != sysinfo_msg:
                Log.log("sysinfo_msg: " + str(sysinfo_msg.hw_info))
                label_text += "\nhw_info: {0}".format(sysinfo_msg.hw_info)

            self.ws_test.configure(text = label_text)
            self.after(100, self.refresh)

    def activate(self):
        Log.log("Activate called")
        self.ws_header = ttk.Label(self, text = "Sensor data", anchor = "nw", width = 20)
        self.ws_header.grid(row = 0 , column = 0)
        self.ws_test = ttk.Label(self, text = "Distance: {0}".format(0), anchor = "nw", width = 20)
        self.ws_test.grid(row = 1, column = 0)
        self.active = True
        self.after(100, self.refresh)

    def pause(self):
        Log.log("Pause called")
        self.active = False

    def deactivate(self):
        Log.log("Deactivate called")
        WorkspaceBase.destroy(self)
        self.active = False