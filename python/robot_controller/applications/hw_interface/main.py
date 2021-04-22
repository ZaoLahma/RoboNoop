from ...core.comm.comm_endpoint import CommEndpoint
from ...core.comm.core_messages import ALL_CORE_MESSAGES
from ...core.comm.message_protocol import MessageProtocol
from ...core.runtime.scheduler import Scheduler
from ...core.runtime.scheduler_network import SchedulerNetwork
from ...core.log.log import Log
from ...core.driver.hcsr04.task.distance_task import DistanceTask
from ...core.driver.l298n.task.motor_controller_task import MotorControllerTask
from ...core.driver.mcu.task.hwinfo_task import HwInfoTask
from ...core.driver.mcu.task.temperature_task import TemperatureTask
from .task.driver_context import DriverContext
from .task.hw_interface_task import HwInterfaceTask
from .comm.hw_if_messages import ALL_COMMAND_MESSAGES

class Main:
    @staticmethod
    def run():
        Log.log_file_name = "hw_interface.log"
        Log.log_application_name = "hw_if"
        Log.log("HW_INTERFACE application starting...")

        protocol = MessageProtocol(ALL_CORE_MESSAGES + ALL_COMMAND_MESSAGES)
        comm_task = CommEndpoint([protocol])

        driver_ctxt = DriverContext()

        temp_task = TemperatureTask()
        hwinfo_task = HwInfoTask()
        distance_task = DistanceTask()
        motor_controller_task = MotorControllerTask()
        hw_interface_task = HwInterfaceTask(comm_task, driver_ctxt)

        driver_ctxt.add_driver("temp", temp_task)
        driver_ctxt.add_driver("distance", distance_task)
        driver_ctxt.add_driver("motor", motor_controller_task)
        driver_ctxt.add_driver("hwinfo", hw_interface_task)

        scheduler = Scheduler("HW_IF", [comm_task, distance_task, motor_controller_task, temp_task, hwinfo_task, hw_interface_task])

        run_in_new_thread = False
        inactivity_timeout = 1
        thread = SchedulerNetwork(scheduler, comm_task, run_in_new_thread, inactivity_timeout)
        Log.log("STARTING SCHEDULER")
        thread.start()

if "__main__" == __name__:
    Main.run()