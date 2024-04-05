try:
    import RPi.GPIO as GPIO
    import pigpio
except ImportError:
    # We're not on a Raspberry Pi - use a mock GPIO
    from utils.mock_imports import MockGPIO as GPIO
import time
import json
from pathlib import Path


state_path = Path(__file__).parent / "state/state.json"
servo = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(servo, GPIO.OUT)
# in servo motor,
# 1ms pulse for 0 degree (LEFT)
# 1.5ms pulse for 90 degree (MIDDLE)
# 2ms pulse for 180 degree (RIGHT)

# so for 50hz, one frequency is 20ms
# duty cycle for 0 degree = (1/20)*100 = 5%
# duty cycle for 90 degree = (1.5/20)*100 = 7.5%
# duty cycle for 180 degree = (2/20)*100 = 10%


class Gripper:
    def __init__(self, pin, pwm=50):
        """
        Initializes the Gripper

        Args:
            pin ():
            pwm (int): Pule width modulation for servo
        """

        self.pwm = pigpio.pi()
        self.pwm.set_mode(servo, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(servo, 50)
        self.pin = pin
        # self.pwm = pwm
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.pin, GPIO.OUT)
        # self.p = GPIO.PWM(self.pin, pwm)  # 50hz frequency
        # self.p.start(2.5)
        self.is_closed = False  # grip state

        # read the state.json file and update the gripper state
        with open(state_path, "r") as f:
            state = json.load(f)
            if state["gripper"] == "closed":
                self.is_closed = True
                self.ungrip()

    def __del__(self):
        """
        Destructor

        Ensures that GPIO is cleaned up properly. TODO: might have to check if this
        interferes with the other modules connected to GPIO...
        """

        self.pwm.set_servo_pulsewidth(servo, 0)
        GPIO.cleanup()

    def grip(self):
        """
        Makes gripper grip
        """
        if self.is_closed:
            raise Exception("Gripper is already closed")

        # for _ in range(3):
            # self.p.ChangeDutyCycle(2.5)  # grip
        self.pwm.set_servo_pulsewidth(servo, 2000)
        time.sleep(0.5)
            # print("gyyat")

        self.is_closed = True

        # update the state.json file
        with open(state_path, "r") as f:
            state = json.load(f)
            state["gripper"] = "closed"

        with open(state_path, "w") as f:
            json.dump(state, f, indent=4)

    def ungrip(self):
        """
        Makes gripper ungrip
        """
        if not self.is_closed:
            raise Exception("Gripper is already open")

        # for _ in range(3):
            # self.p.ChangeDutyCycle(3.9)  # ungrip
        self.pwm.set_servo_pulsewidth(servo, 500)
        time.sleep(0.5)
        print("ungrip")

        self.is_closed = False

        # update the state.json file
        with open(state_path, "r") as f:
            state = json.load(f)
            state["gripper"] = "open"

        with open(state_path, "w") as f:
            json.dump(state, f, indent=4)
