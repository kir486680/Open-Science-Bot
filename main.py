import numpy as np 
from lego_brain import Gantry
import concurrent.futures
from pump import Pump
from camera import Camera
from gripper import Gripper
import threading
import cv2
from tasks import GripperTask, PumpTask, CameraTask, MoveRobotTask
#init the main 


def main():
    gantry = Gantry()
    pump = Pump([23,24,25])
    camera = Camera()
    gantry.set_cm_per_rotation([4, 12.56, 5])
    gripper = Gripper(17)
    

    gripper_task = GripperTask(gripper)
    #pump_task = PumpTask(pump)
    camera_task = CameraTask(camera)
    move_robot_task = MoveRobotTask(gantry)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(gripper_task.execute())
        #executor.submit(pump_task.execute())
        executor.submit(camera_task.execute())
        executor.submit(move_robot_task.execute())

        concurrent.futures.wait([gripper_task, camera_task, move_robot_task])


if __name__ == "__main__":
    main()