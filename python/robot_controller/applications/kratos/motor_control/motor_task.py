from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from ....core.state.state import State
from ....core.state.state import StateHandler
from ...daredevil.sonar_control.sonar_control_messages import SonarDataInd
from .motor_controller import MotorController
import time

# This desperately needs a magnetometer to be more sane in its decision making
class MotorTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if

        self.state_def =  [
            State("INIT", self.handle_init, "CONNECT_DAREDEVIL", "INIT"),
            State("CONNECT_DAREDEVIL", self.handle_connect_daredevil, "ENABLED", "INIT"),
            State("ENABLED", self.handle_enabled, "ENABLED", "INHIBITED"),
            State("PAN", self.handle_pan, "ENABLED", "INHIBITED"),
            State("AVOID_COLLISION", self.handle_avoid_collision, "CHECK_LEFT", "REVERSE"),
            State("REVERSE", self.handle_reverse, "CHECK_LEFT", "INHIBITED"),
            State("CHECK_LEFT", self.handle_check_left, "COOLDOWN", "INHIBITED"),
            State("RESET_LEFT", self.handle_reset_left, "COOLDOWN", "INHIBITED"),
            State("CHECK_RIGHT", self.handle_check_right, "COOLDOWN", "INHIBITED"),
            State("RESET_RIGHT", self.handle_reset_right, "COOLDOWN", "INHIBITED"),
            State("SOLVE_COLLISION", self.handle_solve_collision, "ENABLED", "INHIBITED"),
            State("COOLDOWN", self.handle_cooldown, "STATE_DEFINED", "INHIBITED"),
            State("INHIBITED", self.handle_inhibited, "ENABLED", "INIT")
        ]
        self.state_handler = StateHandler(self.state_def, "INIT")

        self.motor_controller = MotorController()

        self.state_start_time = None
        self.state_end_time = None
        self.state_time_to_run = None
        self.state_cooldown_time = 1
        self.state_post_cooldown = None
        self.state_cooldown_start_time = None

        self.state_check_left_distance = None
        self.state_check_right_distance = None

        self.pan_direction = "LEFT"

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
        if None == self.state_start_time:
            self.state_start_time = time.time()
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())
        if None != msg:
            Log.log("Motor task receiving sonar data")
            #Zig every 1.5 seconds
            max_time_to_pan = 1.5
            if time.time() - self.state_start_time >= max_time_to_pan:
                self.motor_controller.stop()
                self.state_start_time = None
                self.state_handler.transition_to("PAN")
            if 300 > msg.distance:
                Log.log("Too close to object - avoid collision")
                self.state_start_time = None
                self.state_handler.transition_to("AVOID_COLLISION")
        else:
            Log.log("Motor task not receiving sonar data")

    def handle_pan(self):
        if None == self.state_start_time:
            self.state_start_time = time.time()
        if self.pan_direction == "LEFT":
            self.motor_controller.turn_left()
        else:
            self.motor_controller.turn_right()
        pan_time = 0.2
        if time.time() - self.state_start_time > pan_time:
            if self.pan_direction == "LEFT":
                self.pan_direction = "RIGHT"
            else:
                self.pan_direction = "LEFT"
            self.state_start_time = None
            self.motor_controller.forward()
            self.state_handler.transition_to("ENABLED")

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
                self.state_end_time = time.time()
                self.state_check_left_distance = msg.distance
                self.state_post_cooldown = "RESET_LEFT"
                self.state_handler.transition()

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
            self.state_post_cooldown = "CHECK_RIGHT"
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
                self.state_end_time = time.time()
                self.state_check_right_distance = msg.distance
                self.state_post_cooldown = "RESET_RIGHT"
                self.state_handler.transition()

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
            self.state_post_cooldown = "SOLVE_COLLISION"
            self.state_handler.transition()

    def handle_solve_collision(self):
        if None == self.state_start_time:
            self.state_start_time = time.time()
        if self.state_check_left_distance > self.state_check_right_distance:
            Log.log("Solve left")
            self.motor_controller.turn_left()
        else:
            Log.log("Solve right")
            self.motor_controller.turn_right()
        msg = self.comm_if.get_message(SonarDataInd.get_msg_id())

        if None != msg:
            #Turn for at least a fifth of a second since we don't really know how we've been turning
            min_time = 0.2
            if msg.distance >= 300 and time.time() - self.state_start_time >= min_time:
                self.state_start_time = None
                #Ugly hack until exploration is implemented
                self.motor_controller.forward()
                self.state_handler.transition()


    def handle_cooldown(self):
        if None == self.state_cooldown_start_time:
            self.state_cooldown_start_time = time.time()

        if time.time() - self.state_cooldown_start_time >= self.state_cooldown_time:
            self.state_cooldown_start_time = None
            self.state_handler.transition_to(self.state_post_cooldown)

    def handle_inhibited(self):
        Log.log("Inhibited")
