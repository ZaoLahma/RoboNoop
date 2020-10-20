from ....core.runtime.task_base import TaskBase
from ....core.comm.core_messages import DataTransfer
from ....core.log.log import Log

class SysinfoTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if
        self.hw_info = self.get_hw_info()
        Log.log("hw_info: " + str(self.hw_info))


    def run(self):
        data_transfer = DataTransfer()
        data_transfer.add_data("hw-type", self.hw_info)
        

    def get_hw_info(self):
        hw_info = ""
        try:
            f = open('/sys/firmware/devicetree/base/model', 'r')
            for line in f:
                hw_info = line
                break
            f.close()
        except:
            hw_info = "stubbed"
        return hw_info
