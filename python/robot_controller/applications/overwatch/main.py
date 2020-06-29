from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_thread import SchedulerThread
from ...core.log.log import Log
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from .comm_listener.comm_listener_task import CommListenerTask
from time import sleep

class Main:
    @staticmethod
    def run():
        print("Overwatch application starting...")

        Log.log_file_name = "overwatch.log"

        protocol = MessageProtocol(ALL_CORE_MESSAGES)

        comm_task = CommEndpoint([protocol])
        comm_listener_task = CommListenerTask(comm_task)

        tasks = []
        tasks.append(comm_task)
        tasks.append(comm_listener_task)

        scheduler = Scheduler("Overwatch", tasks)

        run_in_new_thread = False
        thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 50
        thread.start(scheduler_periodicity_ms)