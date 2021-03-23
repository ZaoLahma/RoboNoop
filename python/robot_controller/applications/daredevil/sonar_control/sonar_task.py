from ....core.runtime.task_base import TaskBase
from ....core.log.log import Log
from .sonar_control_messages import SonarDataInd

try:
    import RPi.GPIO as GPIO
except ImportError:
    from ....core.runtime.gpio_stub import GPIOStub as GPIO

from time import time
from time import sleep
from threading import Lock

class SonarTask(TaskBase):
    INIT_PULSE = 0
    WAIT_FOR_PULSE_START = 1
    WAIT_FOR_PULSE_END = 2
    PULSE_END = 3
    def __init__(self, comm_if):
        self.comm_if = comm_if
        self.trig_pin = 11
        self.echo_pin = 13

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.add_event_detect(self.echo_pin, GPIO.BOTH, callback=self.pin_callback)

        self.pulse_start = time()
        self.pulse_end = time()

        self.pin_states = [SonarTask.INIT_PULSE, SonarTask.WAIT_FOR_PULSE_START, SonarTask.WAIT_FOR_PULSE_END, SonarTask.PULSE_END]
        self.pin_state = 0

        self.interrupt_lock = Lock()

    def pin_callback(self, pin):
        self.interrupt_lock.acquire()
        if SonarTask.WAIT_FOR_PULSE_START == self.pin_states[self.pin_state]:
            if 1 == GPIO.input(self.echo_pin):
                self.pulse_start = time()
                self.pin_state += 1
            else:
                #Pin toggled back to 0 before we had the chance to read it.
                #We're CLOSE to something. Set pulse_end and set state to
                #PULSE_END asap
                self.pulse_end = time()
                self.pin_state += 2

        elif SonarTask.WAIT_FOR_PULSE_END == self.pin_states[self.pin_state]:
            if 0 == GPIO.input(self.echo_pin):
                self.pulse_end = time()
                self.pin_state += 1
        else:
            pass
        self.interrupt_lock.release()

    def run(self):
        self.interrupt_lock.acquire()
        Log.log("Curr state: " + str(self.pin_states[self.pin_state]))
        if SonarTask.INIT_PULSE == self.pin_states[self.pin_state]:
            GPIO.output(self.trig_pin, GPIO.HIGH)
            sleep(0.00001)
            GPIO.output(self.trig_pin, GPIO.LOW)
            self.pin_state += 1
        elif SonarTask.PULSE_END == self.pin_states[self.pin_state]:
            pulse_duration = self.pulse_end - self.pulse_start
            distance = int(round(pulse_duration * 171500, 0))
            sonar_msg = SonarDataInd(distance)
            self.comm_if.send_message(sonar_msg)
            self.pin_state = 0
        self.interrupt_lock.release()

