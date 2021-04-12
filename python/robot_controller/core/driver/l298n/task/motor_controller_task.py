from ....runtime.task_base import TaskBase
from ....state.state import State
from ....state.state import StateHandler
from ....log.log import Log
from .motor_controller import MotorController

from time import time
from threading import Lock

class MotorControllerTask(TaskBase):
    FORWARD = 0
    BACKWARD = 1
    LEFT = 2
    RIGHT = 3
    STOP = 4
    def __init__(self):
        TaskBase.__init__(self)

        self.motor_controller = MotorController()

        self.command_to_controller = {}
        self.command_to_controller[MotorControllerTask.FORWARD] = self.motor_controller.forward
        self.command_to_controller[MotorControllerTask.BACKWARD] = self.motor_controller.backward
        self.command_to_controller[MotorControllerTask.LEFT] = self.motor_controller.turn_left
        self.command_to_controller[MotorControllerTask.RIGHT] = self.motor_controller.turn_right
        self.command_to_controller[MotorControllerTask.STOP] = self.motor_controller.stop
        
        self.set_command(MotorControllerTask.STOP)
        self.curr_command()

        self.state_def =  [
            State("ENABLED", self.handle_enabled, "ENABLED", "INHIBITED"),
            State("INHIBITED", self.handle_inhibited, "ENABLED", "INHIBITED")
        ]
        self.state_handler = StateHandler(self.state_def, "INHIBITED")

        self.distance = None
        self.distance_timestamp = None
        self.distance_max_age = 0.5

        self.distance_min = 300
    
    def set_command(self, command):
        self.curr_command = self.command_to_controller[command]

    def run(self):
        func = self.state_handler.get_state_func()
        func()

    def handle_enabled(self):
        success = None != self.distance
        success = success and None != self.distance_timestamp
        success = success and (time() - self.distance_timestamp < self.distance_max_age)
        if True == success:
            if self.distance > self.distance_min or self.curr_command == self.motor_controller.backward:
                self.curr_command()
            else:
                self.motor_controller.stop()
        fail = False == success
        self.state_handler.transition(fail)

    def handle_inhibited(self):
        self.motor_controller.stop()
        success = None != self.distance
        success = success and None != self.distance_timestamp
        success = success and (time() - self.distance_timestamp < self.distance_max_age)
        fail = False == success
        self.state_handler.transition(fail)

    def distance_hook(self, distance):
        self.distance_timestamp = time()
        self.distance = distance