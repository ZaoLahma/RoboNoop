from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_thread import SchedulerThread
from ...core.log.log import Log
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from .motor_control.motor_control_messages import ALL_MOTOR_CONTROL_MESSAGES
from time import sleep

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "kratos.log"
        Log.log("Kratos application starting...")

        protocol = MessageProtocol(ALL_CORE_MESSAGES + ALL_MOTOR_CONTROL_MESSAGES)

        comm_task = CommEndpoint([protocol])
        comm_task.publish_service(3031)

        tasks = []
        tasks.append(comm_task)

        scheduler = Scheduler("Kratos", tasks)

        run_in_new_thread = False
        thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 100
        thread.start(scheduler_periodicity_ms)