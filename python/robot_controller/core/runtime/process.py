from multiprocessing import Process
from ..log.log import Log

class ProcessManager:
    def __init__(self):
        self.processes = []

    def start_process(self, process_name, process_func):
        process = Process(target=process_func)
        self.processes.append((process_name, process))
        process.start()
        Log.log("Started " + process_name + "...")

