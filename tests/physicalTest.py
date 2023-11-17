import numpy as np
import cv2
from autolab.lego_brain import Gantry
from autolab.pump import Pump
from autolab.camera import Camera
from autolab.gripper import Gripper
import time

# init the main


def test_right_gripper():
    gantry = Gantry()
    #Initializing the pump with the defaul GPIO pins
    
    #camera = Camera()
    gantry.set_cm_per_rotation([4, 12.56, 5,5])
    #gripper = Gripper(17)
    #gripper.grip()
    #gripper.ungrip()
    #first parameter in array is x, second is y, third is z of the gripper with counter electrode, fourth is z of gripper with working electrode
    target_position = np.array([0, 0, 0, 0])
    gantry.move_to_position(target_position)
    target_position = np.array([1.5, 0, 2.5, 0])
    gantry.move_to_position(target_position)
    target_position = np.array([0, 0, 3.5, 0])
    gantry.move_to_position(target_position)
    target_position = np.array([0, 0, 0, 0])
    gantry.move_to_position(target_position)
    #gripper.ungrip()
    # image = camera.get_image()
    # cv2.imshow("image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



if __name__ == "__main__":
    for i in range(10):
        test_right_gripper()
