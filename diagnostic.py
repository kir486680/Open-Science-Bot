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
y_wheels = hub.port.A.motor

dist = dist2deg(2,4.2)
wheels_y = hub.port.A.motor
wheels_y.run_for_degrees(-8, 30)  
# -, - -> 
# +, - -> 
#+, + <-
#-, + <-

"""
print(gripper.get())
gripper.run_for_degrees(-20,-30)
print(gripper.get())
time.sleep(1)
gripper.run_for_degrees(20,30)
print(gripper.get())
"""

