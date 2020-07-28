from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_thread import SchedulerThread
from ...core.log.log import Log
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from .sonar_control.sonar_task import SonarTask
from time import sleep

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "daredevil.log"
        Log.log("Daredevil application starting...")

        protocol = MessageProtocol(ALL_CORE_MESSAGES)

        comm_task = CommEndpoint([protocol])
        comm_task.publish_service(3033)

        sonar_task = SonarTask()

        tasks = []
        tasks.append(comm_task)
        tasks.append(sonar_task)

        scheduler = Scheduler("Daredevil", tasks)

        run_in_new_thread = False
        thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 100
        thread.start(scheduler_periodicity_ms)