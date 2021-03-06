from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_thread import SchedulerThread
from ...core.log.log import Log
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from ...core.config.config import Config
from ..daredevil.sonar_control.sonar_control_messages import ALL_SONAR_MESSAGES
from .fear_control.fear_task import FearTask
from time import sleep

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "fear.log"
        Log.log_application_name = "fear"
        Log.log("Fear application starting...")

        protocol = MessageProtocol(ALL_CORE_MESSAGES + ALL_SONAR_MESSAGES)

        comm_task = CommEndpoint([protocol])
        app_config = Config.get_config_val("application")
        port_no = app_config["comm"]["fear"]["port-no"]
        comm_task.publish_service(port_no)

        fear_task = FearTask(comm_task)

        tasks = []
        tasks.append(comm_task)
        tasks.append(fear_task)

        scheduler = Scheduler("Fear", tasks)

        run_in_new_thread = False
        thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 100
        thread.start(scheduler_periodicity_ms)