from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_thread import SchedulerThread
from ...core.log.log import Log
try:
    import RPi.GPIO as GPIO
except ImportError:
    from ...core.runtime.gpio_stub import GPIOStub as GPIO
from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.message_protocol import MessageProtocol
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from ..kratos.motor_control.motor_control_messages import ALL_MOTOR_CONTROL_MESSAGES
from .masterchief import MasterChief
from time import sleep

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "masterchief.log"

        Log.log("MasterChief application starting...")

        GPIO.cleanup()

        protocol = MessageProtocol(ALL_CORE_MESSAGES + ALL_MOTOR_CONTROL_MESSAGES)

        comm_task = CommEndpoint([protocol])

        master_chief = MasterChief(comm_task)

        tasks = []
        tasks.append(comm_task)
        tasks.append(master_chief)

        scheduler = Scheduler("MasterChief", tasks)

        run_in_new_thread = False
        thread = SchedulerThread(scheduler, run_in_new_thread)
        scheduler_periodicity_ms = 100
        thread.start(scheduler_periodicity_ms)