from threading import Thread
from ..log.log import Log

class SchedulerThread(Thread):
    def __init__(self, scheduler, start_thread):
        Thread.__init__(self)
        self.scheduler = scheduler
        self.start_thread = start_thread
        self.active = False

    def run(self):
        Log.log("Thread running for " + self.scheduler.context_name + "...")
        self.active = True
        while True == self.active:
            self.scheduler.run()
    
    def start(self):
        if True == self.start_thread:
            Log.log("Starting thread for scheduler " + self.scheduler.context_name + "...")
            Thread.start(self)
        else:
            self.run()

    def stop(self):
        Log.log("Stop called for " + self.scheduler.context_name + "...")
        self.active = False


    