import numpy as np
from mindstorms import Motor,Hub
import time

hub = Hub()
time.sleep(1)

class GantryRobot:
    def __init__(self, gear_ratios, motor_resolution=360):
        self.gear_ratios = np.array(gear_ratios)  # gear ratios for rack and pinion in X, Y, Z
        self.motor_resolution = motor_resolution  # degrees of rotation for one full rotation of the motor
        self.cm_per_rotation = np.array([1, 1, 1])  # cm moved per full rotation of the gear in X, Y, Z
        self.current_position = np.array([0, 0, 0])  # current position of the robot in cm
        self.motors = [hub.port.A.motor, hub.port.B.motor, hub.port.D.motor]  # adjust motor ports as needed
        self.motors[0].run_at_speed(20)
        self.motors[1].run_at_speed(20)
        self.motors[2].run_at_speed(20)

    def set_cm_per_rotation(self, cm_per_rotation):
        # set cm moved per full rotation of the gear in X, Y, Z
        self.cm_per_rotation = np.array(cm_per_rotation)

    def motor_to_cm(self, motor_rotations):
        # convert motor rotation to cm
        gear_rotations = motor_rotations / self.gear_ratios
        distances_moved = gear_rotations * self.cm_per_rotation
        return distances_moved

    def cm_to_motor(self, distances_cm):
        # convert cm to motor rotation
        gear_rotations = distances_cm / self.cm_per_rotation
        motor_rotations = gear_rotations * self.gear_ratios
        return motor_rotations

    def forward_kinematics(self, motor_rotations):
        # calculate forward kinematics
        self.current_position = self.motor_to_cm(motor_rotations)
        return self.current_position

    def inverse_kinematics(self, target_position):
        # calculate inverse kinematics
        motor_rotations = self.cm_to_motor(target_position - self.current_position)
        self.current_position = target_position
        return motor_rotations

    def move_to_position(self, target_position):
        # move motors to target position
        motor_rotations = self.inverse_kinematics(target_position)
        print(f"Motor rotations: {motor_rotations}")
        for motor, rotation in zip(self.motors, motor_rotations):
            motor.run_to_position(rotation)

# Example usage
robot = GantryRobot(gear_ratios=[1, 1, 1])  # adjust gear_ratios as needed
robot.set_cm_per_rotation([4, 4, 1])  # adjust cm_per_rotation as needed
target_position = np.array([10, 20, 30])  # target position in cm
robot.move_to_position(target_position)
print(f"Current position after movement: {robot.current_position}")
