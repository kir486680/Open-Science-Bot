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
arm = hub.port.B.motor #the highest it goes is  -120
x_wheels = hub.port.E.motor
# - - -> forward 
# + - -> forward 
# - + <- back 
# + + -< back
y_wheels = hub.port.A.motor
# -, - -> 
# +, - -> 
#+, + <-
#-, + <-
x_wheels.run_for_degrees(-270, -30) 
time.sleep(2)
x_wheels.run_for_degrees(270, -30)
time.sleep(2)
x_wheels.run_for_degrees(-270, 30)
time.sleep(2)
x_wheels.run_for_degrees(270, 30)

"""
print(gripper.get())
gripper.run_for_degrees(-20,-30)
print(gripper.get())
time.sleep(1)
gripper.run_for_degrees(20,30)
print(gripper.get())
"""

