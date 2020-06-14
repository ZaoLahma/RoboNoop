from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_thread import SchedulerThread
from ...core.log.log import Log
from time import sleep

class Main:
    @staticmethod
    def run():
        print("Garrus application starting...")

        Log.log_file_name = "garrus.log"

        scheduler = Scheduler("Garrus", [])

        run_in_new_thread = True
        thread = SchedulerThread(scheduler, run_in_new_thread)
        thread.start()

        sleep(2)

        thread.stop()