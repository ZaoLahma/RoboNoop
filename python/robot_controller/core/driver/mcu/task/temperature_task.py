from ....runtime.task_base import TaskBase
from ....log.log import Log

class TemperatureTask(TaskBase):
    def __init__(self):
        TaskBase.__init__(self)
        self.temperature = self.get_temperature()

    def run(self):
        self.temperature = self.get_temperature()
        Log.log("temperature: " + str(self.temperature))

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