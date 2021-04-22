from ....runtime.task_base import TaskBase
from ....log.log import Log

from math import ceil

class TemperatureTask(TaskBase):
    def __init__(self):
        TaskBase.__init__(self)
        self.temperature_hooks = []

    def register_temperature_hook(self, hook):
        self.temperature_hooks.append(hook)

    def run(self):
        temperature = self.get_temperature()
        Log.log("temperature: " + str(temperature))
        for hook in self.temperature_hooks:
            hook(temperature)

    def get_temperature(self):
        temp = ""
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = f.read()
                temp = str(ceil(int(temp) / 1000.0))
                f.close()
        except Exception as e:
            temp = "UNAVAILABLE"
        return temp