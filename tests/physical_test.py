import numpy as np
import cv2
from autolab.lego_brain import Gantry
from autolab.pump import Pump
from autolab.camera import Camera
from autolab.gripper import Gripper
import time

# init the main


def test_left_gripper():
    gantry = Gantry()
    gantry.set_cm_per_rotation([4, 12.56, 5, 5])
    target_position = np.array([0, 0, 0, 1.0])
    gantry.move_to_position(target_position)
    target_position = np.array([0, 0, 0, 0])
    gantry.move_to_position(target_position)
    target_position = np.array([0, 0, 0, 2.0])
    gantry.move_to_position(target_position)
    target_position = np.array([0, 0, 0, 0])
    gantry.move_to_position(target_position)
    # target_position = np.array([0, 0, 0, 3.0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([0, 0, 0, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([0, 0, 0, 3.5])
    # gantry.move_to_position(target_position)
    # target_position = np.array([0, 0, 0, 0])
    # gantry.move_to_position(target_position)

def test_right_gripper():
    gantry = Gantry()
    gantry.set_cm_per_rotation([4, 12.56, 5, 5])
    # first parameter in array is x, second is y, third is z of the gripper with counter electrode, fourth is z of gripper with working electrode
    # first well
    target_position = np.array([0, 0, 0, 0])
    gantry.move_to_position(target_position)
    time.sleep(1)
    target_position = np.array([0, 0, 1.0, 0])
    gantry.move_to_position(target_position)
    time.sleep(1)
    target_position = np.array([0, 0, 0, 0])
    gantry.move_to_position(target_position)
    time.sleep(1)
    target_position = np.array([0, 0, 2.0, 0])
    gantry.move_to_position(target_position)
    time.sleep(1)
    target_position = np.array([0, 0, 0, 0])
    gantry.move_to_position(target_position)
    time.sleep(1)
    target_position = np.array([0, 0, 3.5, 0])
    gantry.move_to_position(target_position)
    time.sleep(1)
    target_position = np.array([0, 0, 0, 0])
    gantry.move_to_position(target_position)
    # second well
    # target_position = np.array([6, 0, 2.5, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([4.5, 0, 3.5, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([4.5, 0, 0, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([0, 0, 0, 0])
    # gantry.move_to_position(target_position)

    # third well
    # target_position = np.array([0, 6, 0, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([1.5, 6, 2.5, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([0, 6, 3.5, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([0, 6, 0, 0])
    # gantry.move_to_position(target_position)

    # fourth well
    # target_position = np.array([6, 6, 0, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([4.5, 6, 3.5, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([4.5, 6, 0, 0])
    # gantry.move_to_position(target_position)

    # return to the initial position
    # target_position = np.array([0, 0, 0, 0])
    # gantry.move_to_position(target_position)


if __name__ == "__main__":
    repetitions = 1
    for i in range(repetitions):
        test_right_gripper()
        # test_left_gripper()
