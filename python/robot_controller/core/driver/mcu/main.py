from ...runtime.scheduler import Scheduler
from ...runtime.scheduler_thread import SchedulerThread
from ...log.log import Log
from .task.hwinfo_task import HwInfoTask
from .task.temperature_task import TemperatureTask

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "mcu.log"
        Log.log_application_name = "mcu"
        Log.log("MCU application starting...")

        temp_task = TemperatureTask()
        hwinfo_task = HwInfoTask()

        scheduler = Scheduler("MCU", [temp_task, hwinfo_task])

        run_in_new_thread = False
        thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 200
        thread.start(scheduler_periodicity_ms)

if "__main__" == __name__:
    Main.run()