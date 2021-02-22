from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_thread import SchedulerThread
from ...core.log.log import Log
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from ...core.config.config import Config
from .core.window import Window
from .workspace.ws_start import WsStart
from time import sleep

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "gui.log"

        Log.log("GUI application starting...")

        protocol = MessageProtocol(ALL_CORE_MESSAGES)

        comm_task = CommEndpoint([protocol])

        tasks = []
        tasks.append(comm_task)

        scheduler = Scheduler("GUI", tasks)

        run_in_new_thread = True
        thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 100
        thread.start(scheduler_periodicity_ms)

        Log.log_application_name = "Test"
        Log.log("Starting...")
        window = Window()
        window.add_workspace(WsStart)
        window.activate_workspace(WsStart)

        window.run()