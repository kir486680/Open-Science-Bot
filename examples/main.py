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
    # time.sleep(1)
    #pump2.pump_liquid(10)
    #Initializing the pump with the defaul GPIO pins
    
    
    #camera = Camera()
    gantry.set_cm_per_rotation([4, 12.56, 5,5])
    gripper = Gripper(17)
    #time.sleep(1)
    #target_position = np.array([0, 0, 3.0, 0])
    #gantry.move_to_position(target_position)
    # time.sleep(1)
    #gripper.grip()
    #gripper.ungrip()
    # time.sleep(1)
    # target_position = np.array([0, 0, 0, 0])
    # gantry.move_to_position(target_position)
    # time.sleep(5)
    #first parameter in array is x, second is y, third is z of the gripper with counter electrode, fourth is z of gripper with working electrode
    #target_position = np.array([0, 0, 3.5, 0.0])
    #gantry.move_to_position(target_position)
   
    target_position = np.array([0, 0, 0.0, 0.0])
    gantry.move_to_position(target_position)
    target_position = np.array([5.8, 0, 0.0, 0.0])
    gantry.move_to_position(target_position)
    time.sleep(2)
    target_position = np.array([5.8, 0, 0, 2.5])
    gantry.move_to_position(target_position)
    time.sleep(2)
    gripper.grip()
    time.sleep(2)
    target_position = np.array([5.8, 0, 0.0, 0.0])
    gantry.move_to_position(target_position)
    time.sleep(2)
    target_position = np.array([0, 0, 0.0, 0.0])
    gantry.move_to_position(target_position)
    time.sleep(2)
    target_position = np.array([0, 0, 4.1, 0.0])
    gantry.move_to_position(target_position)
    time.sleep(2)
    #pump2.pump_liquid(55)
    target_position = np.array([0, 0, 4.1, 2.6])
    gantry.move_to_position(target_position)
    print("Measuring ")
    time.sleep(100)
    #we do measurement here
    target_position = np.array([0, 0, 0.0,0.0])
    gantry.move_to_position(target_position)
    time.sleep(2)
    target_position = np.array([5.8, 0, 0.0, 0.0])
    gantry.move_to_position(target_position)
    time.sleep(2)
    target_position = np.array([5.8, 8.0, 0.0, 0.0])
    gantry.move_to_position(target_position)
    time.sleep(2)
    target_position = np.array([5.8, 8.0, 0.0, 2.0])
    gantry.move_to_position(target_position)
    time.sleep(2)
    gripper.ungrip()
    time.sleep(2)
    target_position = np.array([5.8, 8.0, 0.0, 0.0])
    gantry.move_to_position(target_position)
    time.sleep(2)
    target_position = np.array([0, 0.0, 0.0, 0.0])
    gantry.move_to_position(target_position)
    time.sleep(2)


    # image = camera.get_image()
    # cv2.imshow("image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
