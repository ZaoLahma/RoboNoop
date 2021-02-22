class TaskBase:
    def run(self):
        raise NotImplementedError

    def stop(self):
        return None