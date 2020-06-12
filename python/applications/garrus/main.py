from ..core.runtime.scheduler import Scheduler
from ..core.runtime.scheduler_thread import SchedulerThread
from time import sleep

class Main:
    @staticmethod
    def run():
        print("Garrus application starting...")
        scheduler = Scheduler("Garrus", [])

        thread = SchedulerThread(scheduler, True)
        thread.start()
        sleep(5)
        thread.stop()