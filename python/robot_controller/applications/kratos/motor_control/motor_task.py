from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.state.state import State
from ....core.state.state import StateHandler
from ...daredevil.sonar_control.sonar_control_messages import SonarDataInd
from .motor_controller import MotorController
import time

class MotorTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_init, "CONNECT_DAREDEVIL", "INIT"),
            State("CONNECT_DAREDEVIL", self.handle_connect_daredevil, "ENABLED", "INIT"),
            State("ENABLED", self.handle_enabled, "ENABLED", "INHIBITED"),
            State("AVOID_COLLISION", self.handle_avoid_collision, "CHECK_LEFT", "REVERSE"),
            State("REVERSE", self.handle_reverse, "CHECK_LEFT", "INHIBITED"),
            State("CHECK_LEFT", self.handle_check_left, "RESET_LEFT", "INHIBITED"),
            State("RESET_LEFT", self.handle_reset_left, "CHECK_RIGHT", "INHIBITED"),
            State("CHECK_RIGHT", self.handle_check_right, "RESET_RIGHT", "INHIBITED"),
            State("RESET_RIGHT", self.handle_reset_right, "SOLVE_COLLISION", "INHIBITED"),
            State("SOLVE_COLLISION", self.handle_solve_collision, "ENABLED", "INHIBITED"),
            State("INHIBITED", self.handle_inhibited, "ENABLED", "INIT")
        ]
        self.state_handler = StateHandler(self.state_def, "INIT")

        self.motor_controller = MotorController()

        self.state_start_time = None
        self.state_end_time = None
        self.state_time_to_run = None
        self.state_cooldown_time = 0.2 #seconds

    def run(self):
        func = self.state_handler.get_state_func()
        Log.log("Run called " + self.state_handler.curr_state.state_name)
        func()

    def handle_init(self):
        self.state_handler.transition()

    def handle_connect_daredevil(self):
        if False == self.comm_if.is_connected(3033):
            try:
                self.comm_if.connect("localhost", 3033)
                self.state_handler.transition()
            except Exception as e:
                Log.log("Exception when connecting to daredevil: " + str(e))
                self.state_handler.transition(fail=True)
        else:
            self.state_handler.transition()

    def handle_enabled(self):
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            Log.log("Motor task receiving sonar data")
            if 300 > msg.distance:
                Log.log("Too close to object - avoid collision")
                self.state_handler.transition_to("AVOID_COLLISION")
        else:
            Log.log("Motor task not receiving sonar data")

    def handle_avoid_collision(self):
        Log.log("Avoiding collisions")
        self.motor_controller.stop()
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            if 199 < msg.distance:
                self.state_handler.transition()
            else:
                self.state_handler.transition(fail=True)

    def handle_reverse(self):
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            if 200 > msg.distance:
                self.motor_controller.backward()
            else:
                self.motor_controller.stop()
                self.state_handler.transition()

    def handle_check_left(self):
        if None == self.state_start_time:
            self.state_start_time = time.time()
        self.motor_controller.turn_left()
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            Log.log("Check left - Distance: " + str(msg.distance))
            if 300 < msg.distance:
                self.motor_controller.stop()
                if None == self.state_end_time:
                    self.state_end_time = time.time()
                if time.time() - self.state_end_time >= self.state_cooldown_time:
                    self.state_handler.transition()
                else:
                    Log.log("Cooldown check left")

    def handle_reset_left(self):
        if None == self.state_time_to_run:
            self.state_time_to_run = self.state_end_time - self.state_start_time
            Log.log("Reset left time to run: " + str(self.state_time_to_run))
            self.state_start_time = time.time()

        self.motor_controller.turn_right()

        if time.time() - self.state_start_time >= self.state_time_to_run:
            self.motor_controller.stop()
            self.state_start_time = None
            self.state_time_to_run = None
            self.state_end_time = None
            self.state_handler.transition()

    def handle_check_right(self):
        if None == self.state_start_time:
            self.state_start_time = time.time()
        self.motor_controller.turn_right()
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            Log.log("Check right - Distance: " + str(msg.distance))
            if 300 < msg.distance:
                self.motor_controller.stop()
                if None == self.state_end_time:
                    self.state_end_time = time.time()
                if time.time() - self.state_end_time >= self.state_cooldown_time:
                    self.state_handler.transition()
                else:
                    Log.log("Cooldown check right")

    def handle_reset_right(self):
        if None == self.state_time_to_run:
            self.state_time_to_run = self.state_end_time - self.state_start_time
            Log.log("Reset right time to run: " + str(self.state_time_to_run))
            self.state_start_time = time.time()

        self.motor_controller.turn_left()

        if time.time() - self.state_start_time >= self.state_time_to_run:
            self.motor_controller.stop()
            self.state_start_time = None
            self.state_time_to_run = None
            self.state_end_time = None
            self.state_handler.transition()

    def handle_solve_collision(self):
        self.state_handler.transition()
        #implement: Check distances that left and right turns reported and move to target furthest/closest?

    def handle_inhibited(self):
        Log.log("Inhibited")
