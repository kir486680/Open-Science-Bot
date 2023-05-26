import RPi.GPIO as GPIO
from time import sleep
import time 

# in1 = 23
# in2 = 24
# en = 25
# temp1 = 1

class Pump:
    def __inti__(self, pins, pwm = 100, dir = 0):
        """
        Initializing the pump 

        Args:
            pins (dict):  0 in1, 1 in2, 2 en
        """
        try:
          GPIO.setmode(GPIO.BCM)
          GPIO.setup(pins[0],GPIO.OUT)
          GPIO.setup(pins[1],GPIO.OUT)
          GPIO.setup(pins[2],GPIO.OUT)
          GPIO.output(pins[0],GPIO.LOW)
          GPIO.output(pins[1],GPIO.LOW)
          self.pump=GPIO.PWM(pins[2],1000)
          self.pump.start(25)
          self.pwm = pwm
        except:
            print("Not able to initialize the pump. Exiting the script")
            exit()
    def pump(self,amount, duration):
        """
        Pumping

        Args:
            amount (int):  pump amount of liquid in mL
            duraction (float): amount of seconds it should be pumping. Optional
        """
        duration = ((amount* 0.775) + -7.8928) 
        end_time = time.time() + duration  # Calculate the end time
        
        while time.time() < end_time:
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            self.pump.ChangeDutyCycle(self.pwm)
            print("Time left ", time.time() < end_time)
            

