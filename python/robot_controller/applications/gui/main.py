from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_thread import SchedulerThread
from ...core.log.log import Log
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from ...core.config.config import Config
from ...applications.daredevil.sonar_control.sonar_control_messages import ALL_SONAR_MESSAGES
from ...applications.garrus.image_control.image_control_messages import ALL_IMAGE_CONTROL_MESSAGES
from .comm.comm_ctxt import CommCtxt
from .comm.connect_task import ConnectTask
from .core.window import Window
from .workspace.ws_conn_status import WsConnStatus
from .workspace.ws_sensor_data import WsSensorData
from .workspace.ws_image import WsImage
from .workspace.ws_opencv_test import WsOpenCVTest
from time import sleep

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "gui.log"

        Log.log("GUI application starting...")

        protocol = MessageProtocol(ALL_CORE_MESSAGES + ALL_SONAR_MESSAGES + ALL_IMAGE_CONTROL_MESSAGES)

        comm_task = CommEndpoint([protocol])
        connect_task = ConnectTask(comm_task)

        CommCtxt.set_comm_if(comm_task)

        tasks = []
        tasks.append(comm_task)
        tasks.append(connect_task)

        scheduler = Scheduler("GUI", tasks)

        run_in_new_thread = True
        scheduler_thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 100
        scheduler_thread.start(scheduler_periodicity_ms)

        resolution = (640, 500)

        window = Window(resolution)
        window.add_shutdown_hook(scheduler_thread.stop)
        window.add_workspace(WsConnStatus)
        window.add_workspace(WsSensorData)
        window.add_workspace(WsImage)
        window.add_workspace(WsOpenCVTest)
        window.activate_workspace(WsConnStatus)

        window.run()

        Log.log("Main exiting")