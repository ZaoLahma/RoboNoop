from ..log.log import Log

class Scheduler:
    def __init__(self, context_name, tasks):
        self.context_name = context_name
        Log.log("Initializing scheduler for " + context_name + "...")
        self.active = False
        self.tasks = tasks

    def run(self):
        for task in self.tasks:
            task.run()
    
    def stop(self):
        self.active = False