from ....runtime.task_base import TaskBase
from ....log.log import Log

try:
    import RPi.GPIO as GPIO
except ImportError:
    from ...gpio_stub.gpio_stub import GPIOStub as GPIO

from time import time
from time import sleep
from threading import Lock

class DistanceTask(TaskBase):
    INIT_PULSE = 0
    WAIT_FOR_PULSE_START = 1
    WAIT_FOR_PULSE_END = 2
    PULSE_END = 3
    def __init__(self):
        TaskBase.__init__(self)
        
        self.trig_pin = 11
        self.echo_pin = 13

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.add_event_detect(self.echo_pin, GPIO.BOTH, callback=self.pin_callback)

        self.pulse_start = time()
        self.pulse_end = time()

        self.pin_states = [DistanceTask.INIT_PULSE, DistanceTask.WAIT_FOR_PULSE_START, DistanceTask.WAIT_FOR_PULSE_END, DistanceTask.PULSE_END]
        self.pin_state = 0

        self.interrupt_lock = Lock()

        self.distance_hooks = []

    def register_distance_hook(self, hook):
        self.distance_hooks.append(hook)

    def pin_callback(self, pin):
        self.interrupt_lock.acquire()
        if DistanceTask.WAIT_FOR_PULSE_START == self.pin_states[self.pin_state]:
            self.pulse_start = time()
            if 1 == GPIO.input(self.echo_pin):
                self.pin_state += 1
            else:
                #Pin toggled back to 0 before we had the chance to read it.
                #We're CLOSE to something. Set pulse_end to pulse_start and 
                #set state to PULSE_END asap
                self.pulse_end = self.pulse_start
                self.pin_state += 2

        elif DistanceTask.WAIT_FOR_PULSE_END == self.pin_states[self.pin_state]:
            if 0 == GPIO.input(self.echo_pin):
                self.pulse_end = time()
                self.pin_state += 1
        else:
            pass
        self.interrupt_lock.release()

    def run(self):
        self.interrupt_lock.acquire()
        if DistanceTask.INIT_PULSE == self.pin_states[self.pin_state]:
            GPIO.output(self.trig_pin, GPIO.HIGH)
            sleep(0.00001)
            GPIO.output(self.trig_pin, GPIO.LOW)
            self.pin_state += 1
        elif DistanceTask.PULSE_END == self.pin_states[self.pin_state]:
            pulse_duration = self.pulse_end - self.pulse_start
            distance = int(round(pulse_duration * 171500, 0))
            for hook in self.distance_hooks:
                hook(distance)
            self.pin_state = 0
        self.interrupt_lock.release()

