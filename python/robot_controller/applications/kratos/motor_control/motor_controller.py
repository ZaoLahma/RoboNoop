try:
    import RPi.GPIO as GPIO
except ImportError:
    from ....core.runtime.gpio_stub import GPIOStub as GPIO

class MotorController:
    def __init__(self):
        self.right_eng_frwd  = 16
        self.right_eng_bckwd = 18
        self.left_eng_frwd  = 29
        self.left_eng_bckwd = 31

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.right_eng_frwd, GPIO.OUT)
        GPIO.setup(self.right_eng_bckwd, GPIO.OUT)
        GPIO.setup(self.left_eng_frwd, GPIO.OUT)
        GPIO.setup(self.left_eng_bckwd, GPIO.OUT)

        self.stop()

    def stop(self):
        GPIO.output(self.right_eng_frwd, GPIO.LOW)
        GPIO.output(self.right_eng_bckwd, GPIO.LOW)
        GPIO.output(self.left_eng_frwd, GPIO.LOW)
        GPIO.output(self.left_eng_bckwd, GPIO.LOW)

    def forward(self):
        self.stop()
        GPIO.output(self.right_eng_frwd, GPIO.HIGH)
        GPIO.output(self.left_eng_frwd, GPIO.HIGH)

    def backward(self):
        self.stop()
        GPIO.output(self.right_eng_bckwd, GPIO.HIGH)
        GPIO.output(self.left_eng_bckwd, GPIO.HIGH)

    def turn_left(self):
        self.stop()
        GPIO.output(self.left_eng_bckwd, GPIO.HIGH)
        GPIO.output(self.right_eng_frwd, GPIO.HIGH)

    def turn_right(self):
        self.stop()
        GPIO.output(self.right_eng_bckwd, GPIO.HIGH)
        GPIO.output(self.left_eng_frwd, GPIO.HIGH)
