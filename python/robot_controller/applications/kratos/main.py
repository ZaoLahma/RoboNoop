from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_network import SchedulerNetwork
from ...core.log.log import Log
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from ...core.config.config import Config
from .motor_control.motor_control_messages import ALL_MOTOR_CONTROL_MESSAGES
from .motor_control.motor_task import MotorTask
from time import sleep

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "kratos.log"
        Log.log_application_name = "kratos"
        Log.log("Kratos application starting...")

        protocol = MessageProtocol(ALL_CORE_MESSAGES + ALL_MOTOR_CONTROL_MESSAGES)

        comm_task = CommEndpoint([protocol])
        app_config = Config.get_config_val("application")
        port_no = app_config["comm"]["kratos"]["port-no"]
        comm_task.publish_service(port_no)

        motor_task = MotorTask(comm_task)

        tasks = []
        tasks.append(comm_task)
        tasks.append(motor_task)

        scheduler = Scheduler("Kratos", tasks)

        run_in_new_thread = False
        thread = SchedulerNetwork(scheduler, comm_task, run_in_new_thread)
        thread.start()