from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.config.config import Config
from ....core.state.state import State
from ....core.state.state import StateHandler
from ..comm.hw_if_messages import DataTransferMessage

class HwInterfaceTask(TaskBase):
    def __init__(self, comm_if, driver_ctxt):
        TaskBase.__init__(self)
        self.comm_if = comm_if
        self.driver_ctxt = driver_ctxt

        self.monitored_sensors = ["distance", "hw-info", "temp"]

        self.tx_data = {}
        
        for sensor in self.monitored_sensors:
            self.tx_data[sensor] = "UNAVAILABLE"

        states = [
            State("INIT", self.handle_init, "ENABLED", "INIT"),
            State("ENABLED", self.handle_enabled, "ENABLED", "INIT")
        ]
        self.state_handler = StateHandler(states, "INIT")

    def run(self):
        func = self.state_handler.get_state_func()
        func()

    def handle_init(self):
        app_config = Config.get_config_val("application")
        port_no = app_config["comm"]["hw-interface"]["port-no"]
        self.comm_if.publish_service(port_no)

        temp_drv = self.driver_ctxt.get_driver("temp")
        temp_drv.register_temperature_hook(self.temperature_hook)

        distance_drv = self.driver_ctxt.get_driver("distance")
        distance_drv.register_distance_hook(self.distance_hook)

        self.state_handler.transition()

    def handle_enabled(self):
        Log.log("Enabled")
        msg = self.comm_if.get_message(DataTransferMessage.get_msg_id())

        if None != msg:
            Log.log("Message received: " + str(msg.data))
            commands = msg.data["commands"]
        
        tx_msg = DataTransferMessage()
        tx_msg.add_data("sensor-data", self.tx_data)
        self.comm_if.send_message(tx_msg)
        
        self.state_handler.transition()

    def distance_hook(self, distance):
        self.tx_data["distance"] = distance
        Log.log("distance: " + str(distance))

    def temperature_hook(self, temperature):
        Log.log("temp: " + str(temperature))
        self.tx_data["temp"] = temperature

    