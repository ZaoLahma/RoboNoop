from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_network import SchedulerNetwork
from ...core.log.log import Log
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from ...core.config.config import Config
from ..daredevil.sonar_control.sonar_control_messages import ALL_SONAR_MESSAGES
from .fear.fear_task import FearTask
from .hide.hide_task import HideTask
from time import sleep

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "mind.log"
        Log.log_application_name = "mind"
        Log.log("Mind application starting...")

        protocol = MessageProtocol(ALL_CORE_MESSAGES + ALL_SONAR_MESSAGES)

        comm_task = CommEndpoint([protocol])
        app_config = Config.get_config_val("application")
        port_no = app_config["comm"]["mind"]["port-no"]
        comm_task.publish_service(port_no)

        fear_task = FearTask(comm_task)
        hide_task = HideTask(comm_task)

        tasks = []
        tasks.append(comm_task)
        tasks.append(fear_task)
        tasks.append(hide_task)

        scheduler = Scheduler("Mind", tasks)

        run_in_new_thread = False
        inactivity_timeout = 0.1
        thread = SchedulerNetwork(scheduler, comm_task, run_in_new_thread, inactivity_timeout)
        thread.start()