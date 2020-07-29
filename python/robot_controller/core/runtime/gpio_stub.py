from ..log.log import Log

class GPIOStub():
    BOARD = 0
    OUTPUT = 1
    INPUT = 2
    LOW = 0
    HIGH = 1
    @staticmethod
    def setmode(mode):
        Log.log("New mode: " + str(mode))

    @staticmethod
    def setup(pin, mode):
        Log.log("Pin " + str(pin) + " set to " + str(mode))

    @staticmethod
    def output(pin, val):
        Log.log("Pin " + str(pin) + " outputting " + str(val))

    @staticmethod
    def input(pin):
        val = 0
        return val