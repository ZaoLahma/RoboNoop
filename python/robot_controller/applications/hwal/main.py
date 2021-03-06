from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_thread import SchedulerThread
from ...core.log.log import Log
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from ...core.config.config import Config
from .sysinfo.sysinfo_task import SysinfoTask
from time import sleep

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "hwal.log"

        Log.log("HWAL application starting...")

        protocol = MessageProtocol(ALL_CORE_MESSAGES)

        comm_task = CommEndpoint([protocol])
        app_config = Config.get_config_val("application")
        port_no = app_config["comm"]["hwal"]["port-no"]
        comm_task.publish_service(port_no)

        sysinfo_task = SysinfoTask(comm_task)

        tasks = []
        tasks.append(comm_task)
        tasks.append(sysinfo_task)

        scheduler = Scheduler("HWAL", tasks)

        run_in_new_thread = False
        thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 100
        thread.start(scheduler_periodicity_ms)