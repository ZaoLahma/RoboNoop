from threading import Thread

class SchedulerThread(Thread):
    def __init__(self, scheduler, start_thread):
        Thread.__init__(self)
        self.scheduler = scheduler
        self.start_thread = start_thread
        self.active = False

    def run(self):
        print("Thread running for " + self.scheduler.context_name + "...")
        self.active = True
        while True == self.active:
            self.scheduler.run()
    
    def start(self):
        if True == self.start_thread:
            print("Starting thread for scheduler " + self.scheduler.context_name + "...")
            Thread.start(self)
        else:
            self.run()

    def stop(self):
        print("Stop called for " + self.scheduler.context_name + "...")
        self.active = False


    