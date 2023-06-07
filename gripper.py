#import all required libraries
import RPi.GPIO as GPIO
import time


servo = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(servo,GPIO.OUT)
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
  
        self.pin = pin
        self.pwm = pwm
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin,GPIO.OUT)
        self.p=GPIO.PWM(self.pin,pwm)       # 50hz frequency
        self.p.start(2.5)


    def grip(self):
        for _ in range(3):
            self.p.ChangeDutyCycle(1) # grip
            time.sleep(0.5)

    def ungrip(self):
        for _ in range(3):
            self.p.ChangeDutyCycle(5) # ungrip
            time.sleep(0.5)

    def __def__(self):
        self.p.stop()
        GPIO.cleanup()  
           
