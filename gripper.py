try:
    import RPi.GPIO as GPIO
except ImportError:
    # We're not on a Raspberry Pi - use a mock GPIO
    from utils.mock_imports import MockGPIO as GPIO
import time


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

        self.pin = pin
        self.pwm = pwm
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.p = GPIO.PWM(self.pin, pwm)  # 50hz frequency
        self.p.start(2.5)

    def __del__(self):
        """
        Destructor

        Ensures that GPIO is cleaned up properly. TODO: might have to check if this
        interferes with the other modules connected to GPIO...
        """

        self.p.stop()
        GPIO.cleanup()

    def grip(self):
        """
        Makes gripper grip
        """

        for _ in range(3):
            self.p.ChangeDutyCycle(4.8)  # grip
            time.sleep(0.5)

    def ungrip(self):
        """
        Makes gripper ungrip
        """

        for _ in range(3):
            self.p.ChangeDutyCycle(2.0)  # ungrip
            time.sleep(0.5)
