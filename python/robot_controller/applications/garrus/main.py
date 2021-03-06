from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_thread import SchedulerThread
from ...core.log.log import Log
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from ...core.config.config import Config
from .image_control.image_control_task import ImageControlTask
from time import sleep

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "garrus.log"
        Log.log_application_name = "garrus"
        Log.log("Garrus application starting...")

        protocol = MessageProtocol(ALL_CORE_MESSAGES)

        comm_task = CommEndpoint([protocol])
        image_control_task = ImageControlTask(comm_task)

        tasks = []
        tasks.append(comm_task)
        tasks.append(image_control_task)

        scheduler = Scheduler("Garrus", tasks)

        run_in_new_thread = False
        thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 0
        thread.start(scheduler_periodicity_ms)