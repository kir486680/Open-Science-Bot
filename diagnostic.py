import os 
import math 
from mindstorms import Hub
import time
import numpy as np

hub = Hub()
time.sleep(1)


motors = [hub.port.A.motor, hub.port.B.motor, hub.port.D.motor] 
motors[0].run_for_degrees(40, speed=60)
#motors[0].pid(1,2,3)

sensor = hub.port.C.device
while True:
    print(sensor.get())
