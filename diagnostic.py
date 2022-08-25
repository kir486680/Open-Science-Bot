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
# -, - -> 
# +, - -> 
#+, + <-
#-, + <-
print(hub.motion.yaw_pitch_roll())
time.sleep(2)
x_wheels.run_to_position(-200,speed=50)
time.sleep(2)
print(hub.motion.yaw_pitch_roll())
time.sleep(2)
x_wheels.run_to_position(-500,speed=50)
time.sleep(2)
print(hub.motion.yaw_pitch_roll())
"""
print(gripper.get())
gripper.run_for_degrees(-20,-30)
print(gripper.get())
time.sleep(1)
gripper.run_for_degrees(20,30)
print(gripper.get())
"""

