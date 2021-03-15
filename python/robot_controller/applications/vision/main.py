from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_network import SchedulerNetwork
from ...core.log.log import Log
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from ..garrus.image_control.image_control_messages import ALL_IMAGE_CONTROL_MESSAGES
from .task.vision_task import VisionTask
from time import sleep

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "vision.log"
        Log.log_application_name = "vision"
        Log.log("Vision application starting...")

        protocol = MessageProtocol(ALL_CORE_MESSAGES + ALL_IMAGE_CONTROL_MESSAGES)

        comm_task = CommEndpoint([protocol])
        vision_task = VisionTask(comm_task)

        tasks = []
        tasks.append(comm_task)
        tasks.append(vision_task)

        scheduler = Scheduler("Vision", tasks)

        run_in_new_thread = False
        thread = SchedulerNetwork(scheduler, comm_task, run_in_new_thread)
        thread.start()