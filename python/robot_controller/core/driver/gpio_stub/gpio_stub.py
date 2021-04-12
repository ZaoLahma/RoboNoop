from ...log.log import Log

from threading import Thread
from time import sleep

class GPIOInterruptStubThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        Log.log("GPIOInterruptStubThread started")
        self.callbacks = {}
        self.active = False

    def add_callback(self, pin, callback):
        self.callbacks[pin] = callback

    def run(self):
        while True == self.active:
            #Log.log("Interrupt thread running")
            for pin in self.callbacks:
                self.callbacks[pin](pin)
            sleep(0.05)

    def start(self):
        #Log.log("Start called")
        self.active = True
        Thread.start(self)

    def stop(self):
        self.active = False
        

class GPIOStub():
    BOARD = 0
    OUT = 1
    IN = 2
    LOW = 0
    HIGH = 1
    CURR_VAL = 0
    BOTH = 0
    INTERRUPT_THREAD = None
    @staticmethod
    def setmode(mode):
        Log.log("New mode: " + str(mode))

    @staticmethod
    def setup(pin, mode):
        #Log.log("Pin " + str(pin) + " set to " + str(mode))
        return None

    @staticmethod
    def output(pin, val):
        #Log.log("Pin " + str(pin) + " outputting " + str(val))
        return None

    @staticmethod
    def input(pin):
        val = GPIOStub.CURR_VAL
        if 1 == GPIOStub.CURR_VAL:
            GPIOStub.CURR_VAL = 0
        else:
            GPIOStub.CURR_VAL = 1
        #Log.log("input returning: " + str(val))
        return val

    @staticmethod
    def cleanup():
        Log.log("Cleanup")

    @staticmethod
    def add_event_detect(pin, edge_detect, callback):
        if None == GPIOStub.INTERRUPT_THREAD:
            GPIOStub.INTERRUPT_THREAD = GPIOInterruptStubThread()
            GPIOStub.INTERRUPT_THREAD.start()
        GPIOStub.INTERRUPT_THREAD.add_callback(pin, callback)
