from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_thread import SchedulerThread
from ...core.log.log import Log
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from time import sleep

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "garrus.log"

        Log.log("Garrus application starting...")

        protocol = MessageProtocol(ALL_CORE_MESSAGES)

        comm_task = CommEndpoint([protocol])
        comm_task.publish_service(3032)

        tasks = []
        tasks.append(comm_task)

        scheduler = Scheduler("Garrus", tasks)

        run_in_new_thread = False
        thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 100
        thread.start(scheduler_periodicity_ms)