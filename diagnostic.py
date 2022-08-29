import os 
import math 
from mindstorms import Hub
import time
import numpy as np

hub = Hub()
time.sleep(1)

def dist2deg(desiredDistance, diameter):
    distancePerDegree = np.pi * diameter / 360
    return desiredDistance/distancePerDegree

gripper = hub.port.D.motor
arm = hub.port.A.motor #the highest it goes is  -120
x_wheels = hub.port.C.motor
# - - -> forward 
# + - -> forward 
# - + <- back 
# + + -< back
y_wheels = hub.port.F.motor
# -, - -> 
# +, - -> 
#+, + <-
#-, + <-
while True:
    userInput = input("Please enter your command:")
    if userInput.lower() == "done":
        print("Shutting Down")
        break
    try:
        exec(userInput)
    except Exception as e:
        print(e)
        print("Try again!")
