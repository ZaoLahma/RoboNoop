from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from .sysinfo_messages import SysinfoMessage

from math import ceil

class SysinfoTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if
        self.hw_info = self.get_hw_info()
        Log.log("hw_info: " + str(self.hw_info))


    def run(self):
        msg = SysinfoMessage()
        msg.add_sysinfo("hw-info", self.hw_info)
        msg.add_sysinfo("temp", self.get_temperature())
        self.comm_if.send_message(msg)
        
    def get_temperature(self):
        temp = ""
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = f.read()
                temp = str(ceil(int(temp) / 1000.0))
                f.close()
        except:
            temp = "UNAVAILABLE"
        return temp

    def get_hw_info(self):
        hw_info = ""
        try:
            with open('/sys/firmware/devicetree/base/model', 'r') as f:
                for line in f:
                    hw_info = line
                    break
                f.close()
        except:
            hw_info = "stubbed"
        return hw_info
