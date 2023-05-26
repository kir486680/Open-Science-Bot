import numpy as np 
from lego_brain import Gantry
from pump import Pump
from camera import Camera

#init the main 


if __name__ == "__main__":
    gantry = Gantry()
    target_position = np.array([20, 5, 0])
    #gantry.move_to_position(target_position)
    pump = Pump([23,24,25])
    #pump.pump_liquid(50)
    camera = Camera()
    camera.preview_camera()
    print("Hello World")
