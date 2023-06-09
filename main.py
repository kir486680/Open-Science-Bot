import numpy as np 
from lego_brain import Gantry
from pump import Pump
from camera import Camera
from gripper import Gripper
import threading
import cv2
#init the main 


def main():
    gantry = Gantry()
    pump = Pump([23,24,25])
    camera = Camera()
    gantry.set_cm_per_rotation([4, 12.56, 5])
    gripper = Gripper(17)
    

    def grip_task():
        gripper.grip()
    
    def pump_task():
        #pump.pump_liquid(15)
        print("Pumping")
    
    def camera_task():
        image = camera.get_image() 
        print(image.shape)

    def move_robot():
        target_position = np.array([0, 0,4])
        gantry.move_to_position(target_position)
        

    grip_thread = threading.Thread(target = grip_task)
    pump_thread = threading.Thread(target = pump_task)
    camera_thread = threading.Thread(target = camera_task)
    robot_thread = threading.Thread(target=move_robot)

    #start the tasks
    # grip_thread.start()
    # camera_thread.start()
    # robot_thread.start()

    # grip_thread.join()
    # camera_thread.join()
    # robot_thread.join()
    print("all taks done")
    image = camera.get_image() 
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Hello World")


if __name__ == "__main__":
    main()