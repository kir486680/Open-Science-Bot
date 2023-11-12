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
    #pump = Pump([23,24,25])
    #pump.pump_liquid(15)
    #camera = Camera()
    #gantry.set_cm_per_rotation([4, 12.56, 5,5])
    #gripper = Gripper(17)
    #gripper.grip()
    #gripper.ungrip()
    #target_position = np.array([0, 2, 0,0 ])
    #gantry.move_to_position(target_position)
    # target_position = np.array([2.3, 0, 2.5])
    # gantry.move_to_position(target_position)
    # gripper.grip()
    # target_position = np.array([2.3, 0, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([5, 15, 0])
    # gantry.move_to_position(target_position)
    # gripper.ungrip()
    # target_position = np.array([0, 0, 0])
    # gantry.move_to_position(target_position)
    target_position = np.array([0, 0, -2, 2])
    gantry.move_to_position(target_position)
    # gripper.grip()
    # target_position = np.array([0, 0, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([5, 15, 0])
    # gantry.move_to_position(target_position)
    # gripper.ungrip()
    # target_position = np.array([0, 0, 0])
    # gantry.move_to_position(target_position)



    # target_position = np.array([0, 0, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([0, 0, 3.4])
    # gantry.move_to_position(target_position)
    # gripper.grip()
    # target_position = np.array([0, 0, 0])
    # gantry.move_to_position(target_position)

    # target_position = np.array([16, 4, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([16, 4, 4.5])
    # gantry.move_to_position(target_position)
    # time.sleep(3)
    # pump.pump_liquid(50)
    # time.sleep(30)
    # target_position = np.array([16, 4, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([5, 15, 0])
    # gantry.move_to_position(target_position)
    # gripper.ungrip()
    # target_position = np.array([0, 0, 0])
    # gantry.move_to_position(target_position)
    

    # target_position = np.array([0, 20, 4])
    # gantry.move_to_position(target_position)
    # time.sleep(2)
    # target_position = np.array([0, 0, 4])
    # gantry.move_to_position(target_position)
    # time.sleep(2)
    # target_position = np.array([0, 0, 0])
    # gantry.move_to_position(target_position)
    # target_position = np.array([0, 0, 4.5])
    # gantry.move_to_position(target_position)
    # print(gripper.is_closed)
    # gripper.grip()
    # gripper.ungrip()
    # time.sleep(10)
    # gripper.grip()
    # time.sleep(10)
    # gripper.ungrip()
    # image = camera.get_image()
    # cv2.imshow("image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print("Hello World")


if __name__ == "__main__":
    main()
