try:
    import RPi.GPIO as GPIO
except ImportError:
    # We're not on a Raspberry Pi - use a mock GPIO
    class MockGPIO:
        BOARD = "BOARD"
        OUT = "OUT"
        IN = "IN"
        HIGH = "HIGH"
        LOW = "LOW"

        def setmode(self, mode):
            print(f"Setting mode {mode}")

        def setup(self, pin, mode):
            print(f"Setting up pin {pin} with mode {mode}")

        def output(self, pin, state):
            print(f"Setting pin {pin} state to {state}")

        def cleanup(self):
            print("Cleaning up")

        # Add more methods and constants as needed based on what you use from RPi.GPIO.

    GPIO = MockGPIO()

from time import sleep
import time

# in1 = 23
# in2 = 24
# en = 25
# temp1 = 1


class Pump:
    def __init__(self, pins, pwm=100, dir=0):
        """
        Initializing the pump

        Args:
            pins (dict):  0 in1, 1 in2, 2 en
        """
        self.pins = pins
        self.pwm = pwm
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins[0], GPIO.OUT)
        GPIO.setup(self.pins[1], GPIO.OUT)
        GPIO.setup(self.pins[2], GPIO.OUT)
        GPIO.output(self.pins[0], GPIO.LOW)
        GPIO.output(self.pins[1], GPIO.LOW)
        self.pump = GPIO.PWM(self.pins[2], 1000)

    def pump_liquid(self, amount, duration=None):
        """
        Pumping

        Args:
            amount (int):  pump amount of liquid in mL
            duraction (float): amount of seconds it should be pumping. Optional
        """

        self.pump.start(25)
        duration = (amount * 0.775) + -7.8928
        end_time = time.time() + duration  # Calculate the end time

        while time.time() < end_time:
            GPIO.output(self.pins[0], GPIO.HIGH)
            GPIO.output(self.pins[1], GPIO.LOW)
            self.pump.ChangeDutyCycle(self.pwm)
            print("Time left ", time.time() - end_time)
        GPIO.cleanup()
