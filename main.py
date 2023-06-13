import numpy as np
import cv2
from lego_brain import Gantry
from pump import Pump
from camera import Camera
from gripper import Gripper

# init the main


def main():
    gantry = Gantry()
    # pump = Pump([23,24,25])
    # pump.pump_liquid(15)
    camera = Camera()
    gantry.set_cm_per_rotation([4, 12.56, 5])
    gripper = Gripper(17)
    target_position = np.array([0, 0, -4])
    gantry.move_to_position(target_position)
    gripper.ungrip()
    image = camera.get_image()
    print("image shape:", image.shape)


if __name__ == "__main__":
    main()
