from ...runtime.scheduler import Scheduler
from ...runtime.scheduler_thread import SchedulerThread
from ...log.log import Log
from .task.motor_controller_task import MotorControllerTask

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "l298n.log"
        Log.log_application_name = "l298n"
        Log.log("L298N application starting...")

        controller_task = MotorControllerTask()

        scheduler = Scheduler("L298N", [controller_task])

        run_in_new_thread = False
        thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 200
        thread.start(scheduler_periodicity_ms)

if "__main__" == __name__:
    Main.run()