import numpy as np

class GripperTask:
    def __init__(self, gripper):
        self.gripper = gripper
    
    def execute(self):
        self.gripper.grip()

class PumpTask:
    def __init__(self, pump):
        self.pump = pump
    
    def execute(self):
        self.pump.pump_liquid(15)

class CameraTask:
    def __init__(self, camera):
        self.camera = camera
    
    def execute(self):
        image = self.camera.get_image()
        print(image.shape)

class MoveRobotTask:
    def __init__(self, gantry):
        self.gantry = gantry
    
    def execute(self):
        target_position = np.array([0, 0,-4])
        self.gantry.move_to_position(target_position)
