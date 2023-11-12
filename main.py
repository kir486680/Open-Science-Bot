import numpy as np
import cv2
from lego_brain import Gantry
from pump import Pump
from camera import Camera
from gripper import Gripper
import time

# init the main


def main():
    gantry = Gantry()
    #Initializing the pump with the defaul GPIO pins
    #pump = Pump([23,24,25])
    #pump.pump_liquid(15)
    #camera = Camera()
    gantry.set_cm_per_rotation([4, 12.56, 5,5])
    gripper = Gripper(17)
    #gripper.grip()
    #gripper.ungrip()
    #first parameter in array is x, second is y, third is z of the gripper with working electrode, fourth is z of gripper with reference electrode
    target_position = np.array([6.5, 0, 0, 2.5])
    gantry.move_to_position(target_position)
    #gripper.ungrip()
    # image = camera.get_image()
    # cv2.imshow("image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
