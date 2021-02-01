from threading import Thread
from ..log.log import Log
from datetime import datetime
from time import sleep

class SchedulerThread(Thread):
    def __init__(self, scheduler, start_thread):
        Thread.__init__(self)
        self.scheduler = scheduler
        self.start_thread = start_thread
        self.active = False
        self.periodicity = 0

    def run(self):
        Log.log("Thread running for " + self.scheduler.context_name + "...")
        self.active = True
        while True == self.active:
            before = datetime.now()
            self.scheduler.run()
            time_delta = datetime.now() - before
            elapsed_ms = time_delta.total_seconds() * 1000
            if self.periodicity - elapsed_ms > 0:
                sleep((self.periodicity - elapsed_ms) / 1000)
            elif 0 != self.periodicity:
                Log.log("Warning scheduler can't keep up, fired " + str(elapsed_ms - self.periodicity) + " late...")
    
    def start(self, scheduler_peridicity):
        self.periodicity = scheduler_peridicity
        if True == self.start_thread:
            Log.log("Starting thread for scheduler " + self.scheduler.context_name + "...")
            Thread.start(self)
        else:
            self.run()

    def stop(self):
        Log.log("Stop called for " + self.scheduler.context_name + "...")
        self.active = False


    