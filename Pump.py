import RPi.GPIO as GPIO
from time import sleep
import time 

in1 = 23
in2 = 24
en = 25
temp1 = 1




GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    
amountPump = 50
duration = ((amountPump * 0.775) + -7.8928) 
  # Convert milliseconds to seconds

end_time = time.time() + duration  # Calculate the end time

while time.time() < end_time:
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    p.ChangeDutyCycle(100)
    print("forward")