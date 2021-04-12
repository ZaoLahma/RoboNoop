from ...runtime.scheduler import Scheduler
from ...runtime.scheduler_thread import SchedulerThread
from ...log.log import Log
from .task.distance_task import DistanceTask

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "hcsr04.log"
        Log.log_application_name = "hcsr04"
        Log.log("HCSR04 application starting...")

        distance_task = DistanceTask()

        scheduler = Scheduler("HCSR04", [distance_task])

        run_in_new_thread = False
        thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 200
        thread.start(scheduler_periodicity_ms)

if "__main__" == __name__:
    Main.run()