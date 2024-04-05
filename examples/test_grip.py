import numpy as np
import cv2
from autolab.lego_brain import Gantry
from autolab.pump import Pump
from autolab.camera import Camera
from autolab.gripper import Gripper
import time

# init the main


def main():
    pump = Pump([23,24,25])
    pump2 = Pump([7,8,11])
    gantry = Gantry()
    #pump.pump_liquid(20)
    #time.sleep(1)
    #pump2.pump_liquid(50)
    #Initializing the pump with the defaul GPIO pins
    
    
    #camera = Camera()
    gantry.set_cm_per_rotation([4, 12.56, 5,5])
    gripper = Gripper(17)

    gripper.ungrip()


    # image = camera.get_image()
    # cv2.imshow("image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
