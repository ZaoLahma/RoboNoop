from ....runtime.task_base import TaskBase
from ....log.log import Log

class HwInfoTask(TaskBase):
    def __init__(self):
        TaskBase.__init__(self)
        self.hw_info = self.get_hw_info()

        self.hw_info_hooks = []

    def register_hw_info_hook(self, hook):
        self.hw_info_hooks.append(hook)

    def run(self):
        self.hw_info = self.get_hw_info()
        Log.log("hw_info: " + str(self.hw_info))
        for hook in self.hw_info_hooks:
            hook(self.hw_info)

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