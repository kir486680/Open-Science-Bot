import numpy as np 
from lego_brain import Gantry
from pump import Pump
from camera import Camera
from gripper import Gripper
import cv2
#init the main 


if __name__ == "__main__":
    gantry = Gantry()
    gantry.set_cm_per_rotation([4, 12.56, 5])
    target_position = np.array([0, -10,-2])
    gantry.move_to_position(target_position)
    gripper = Gripper(17)
    #gripper.grip()
    #pump = Pump([23,24,25])
    #pump.pump_liquid(15)
    #camera = Camera()
    #image = camera.get_image() 
    # cv2.imshow("image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print("Hello World")
