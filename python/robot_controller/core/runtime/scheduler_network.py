from threading import Thread
from threading import Condition
from ..log.log import Log
from time import time
from time import sleep

class SchedulerNetwork(Thread):
    def __init__(self, scheduler, comm_if, start_thread, inactivity_timeout = 1.0):
        Thread.__init__(self)
        self.scheduler = scheduler
        self.comm_if = comm_if
        self.comm_if.register_nw_activity_hook(self.network_activity_hook)
        self.start_thread = start_thread
        self.inactivity_timeout = inactivity_timeout
        self.network_activity_timestamp = time()
        self.exec_cond = Condition()
        self.should_exec = False
        self.active = False

    def network_activity_hook(self):
        Log.log("Network activity hook called")
        self.network_activity_timestamp = time()
        with self.exec_cond:
            self.should_exec = True
            self.exec_cond.notify

    def run(self):
        Log.log("Thread running for " + self.scheduler.context_name + "...")
        self.active = True
        while True == self.active:
            now = time()
            if (now - self.network_activity_timestamp) >= self.inactivity_timeout or True == self.should_exec:
                self.should_exec = False
                self.scheduler.run()
            with self.exec_cond:
                if False == self.should_exec:
                    Log.log("Waiting for network activity")
                    self.exec_cond.wait(timeout = self.inactivity_timeout)
                    Log.log("Network activity indicated")
        Log.log("Thread exiting for " + self.scheduler.context_name)
    
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
        with self.exec_cond:
            self.exec_cond.notify()
        self.scheduler.stop()