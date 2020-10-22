from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_thread import SchedulerThread
from ...core.log.log import Log
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from ..daredevil.sonar_control.sonar_control_messages import ALL_SONAR_MESSAGES
from ..kratos.motor_control.motor_control_messages import ALL_MOTOR_CONTROL_MESSAGES
from .comm_listener.comm_listener_task import CommListenerTask
from time import sleep

class Main:
    @staticmethod
    def run():
        print("Connection aggregator application starting...")

        Log.log_file_name = "message_proxy.log"

        protocol = MessageProtocol(ALL_CORE_MESSAGES + ALL_SONAR_MESSAGES + ALL_MOTOR_CONTROL_MESSAGES)

        comm_aggregate_endpoint = CommEndpoint([protocol])
        comm_endpoint = CommEndpoint([protocol])
        comm_aggregate_task = CommListenerTask(comm_aggregate_endpoint, comm_endpoint)

        tasks = []
        tasks.append(comm_aggregate_endpoint)
        tasks.append(comm_endpoint)
        tasks.append(comm_aggregate_task)

        scheduler = Scheduler("ConnAggregator", tasks)

        run_in_new_thread = False
        thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 50
        thread.start(scheduler_periodicity_ms)