from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
import time
try:
    import RPi.GPIO as GPIO
except ImportError:
    from ....core.runtime.gpio_stub import GPIOStub as GPIO

from .sonar_control_messages import SonarDataInd

class SonarTask(TaskBase):
    def __init__(self, comm_if):
        self.comm_if = comm_if
        self.trig_pin = 11
        self.echo_pin = 13

    def run(self):
        pulse_start = time.time()
        pulse_end = time.time()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, GPIO.LOW)

        loop_start = time.time()
        while 0 == GPIO.input(self.echo_pin):
            pulse_start = time.time()
            if (pulse_start - loop_start > 1):
                Log.log("Timeout waiting for sonar sensor")
                break

        loop_start = time.time()
        pulse_end = time.time()
        while 1 == GPIO.input(self.echo_pin):
            pulse_end = time.time()
            if (pulse_end - loop_start > 1):
                Log.log("Timeout waiting for sonar sensor to indicate echo end")
                break

        pulse_duration = pulse_end - pulse_start

        distance = int(round(pulse_duration * 171500, 0))

        sonar_msg = SonarDataInd(distance)

        #Log.log("Calculated distance: " + str(distance) + "mm")

        self.comm_if.send_message(sonar_msg)

