import numpy as np 
from lego_brain import Gantry
from pump import Pump
from camera import Camera

#init the main 


if __name__ == "__main__":
    gantry = Gantry()
    gantry.set_cm_per_rotation([4, 12.56, 5])
    target_position = np.array([15, 5,3])
    gantry.move_to_position(target_position)
    pump = Pump([23,24,25])
    pump.pump_liquid(15)
    camera = Camera()
    camera.preview_camera()
    print("Hello World")
