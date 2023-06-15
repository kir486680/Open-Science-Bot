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
    # pump = Pump([23,24,25])
    # pump.pump_liquid(15)
    camera = Camera()
    gantry.set_cm_per_rotation([4, 12.56, 5])
    gripper = Gripper(17)
    target_position = np.array([40, 0, 4])
    gantry.move_to_position(target_position)
    time.sleep(2)
    target_position = np.array([40, 20, 4])
    gantry.move_to_position(target_position)
    time.sleep(2)
    target_position = np.array([0, 20, 4])
    gantry.move_to_position(target_position)
    time.sleep(2)
    target_position = np.array([0, 0, 4])
    gantry.move_to_position(target_position)
    time.sleep(2)
    target_position = np.array([0, 0, 0])
    gantry.move_to_position(target_position)
    # target_position = np.array([0, 0, 4.5])
    # gantry.move_to_position(target_position)
    # gripper.ungrip()
    # image = camera.get_image()
    # cv2.imshow("image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print("Hello World")


if __name__ == "__main__":
    main()
