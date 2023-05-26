import numpy as np
from mindstorms import Motor,Hub
import time


class Gantry:

    def __init__(self, gear_ratios=[1, 1, 1], motor_resolution=360):
        self.gear_ratios = np.array(gear_ratios)  # gear ratios for rack and pinion in X, Y, Z
        self.motor_resolution = motor_resolution  # degrees of rotation for one full rotation of the motor
        self.cm_per_rotation = np.array([1, 1, 1])  # cm moved per full rotation of the gear in X, Y, Z
        self.current_position = np.array([0, 0, 0])  # current position of the robot in cm
        self.hub = None
        try:
            self.hub = Hub()
            time.sleep(1)
            self.motors = [self.hub.port.A.motor, self.hub.port.B.motor, self.hub.port.D.motor]  # adjust motor ports as needed
        except:
            print("No hub found, No motors initialized")
        

    def set_cm_per_rotation(self, cm_per_rotation):
        """
        Set the cm per rotation for the robot
        
        Args:
            cm_per_rotation (list): list of cm per rotation for each axis
        
        Returns:
            None
        """
        self.cm_per_rotation = np.array(cm_per_rotation)

    def motor_to_cm(self, motor_rotations):
        """
        Convert motor rotations to cm

        Args:
            motor_rotations (array): array of motor rotations for each axis

        Returns:
            distances_moved (array): array of distances moved for each axis
        """
        gear_rotations = motor_rotations / self.gear_ratios
        distances_moved = gear_rotations * self.cm_per_rotation
        return distances_moved

    def cm_to_motor(self, distances_cm):
        """
        Convert cm to motor rotations

        Args:
            distances_cm (array): array of distances moved for each axis

        Returns:
            motor_rotations (array): array of motor rotations for each axis
        """
        gear_rotations = distances_cm / self.cm_per_rotation
        motor_rotations = gear_rotations * self.gear_ratios
        return motor_rotations

    def forward_kinematics(self, motor_rotations):
        """
        Calculate forward kinematics

        Args:
            motor_rotations (array): array of motor rotations for each axis

        Returns:
            current_position (array): array of current position for each axis
        """
        self.current_position = self.motor_to_cm(motor_rotations)
        return self.current_position

    def inverse_kinematics(self, target_position):
        """
        Calculate inverse kinematics

        Args:
            target_position (array): array of target position for each axis

        Returns:
            motor_rotations (array): array of motor rotations for each axis
        """
        motor_rotations = self.cm_to_motor(target_position - self.current_position)
        self.current_position = target_position
        return motor_rotations

    def move_to_position(self, target_position):
        '''
        Move the robot to the target position
        
        Args:
            target_position (array): array of target position for each axis

        Returns:
            None
        '''
        if self.hub != None:
            # move motors to target position
            motor_rotations = self.inverse_kinematics(target_position)
            print(f"Motor rotations: {motor_rotations}")
            for motor, rotation in zip(self.motors, motor_rotations):
                print(f"Motor: {motor}, rotation: {rotation}")
                rotation_degrees = rotation * self.motor_resolution  # convert rotations to degrees
                print(f"Rotation degrees: {rotation_degrees}")
                if rotation_degrees >= 0:
                    #pass
                    motor.run_for_degrees(abs(rotation_degrees), speed=-60)
                else:
                    motor.run_for_degrees(abs(rotation_degrees), speed=60)
                time.sleep(1)

    
# Example usage
# robot = Gantry(gear_ratios=[1, 1, 1])  # adjust gear_ratios as needed
# robot.set_cm_per_rotation([4, 12.56, 1])  # adjust cm_per_rotation as needed
# target_position = np.array([20, 20, 0])  # target position in cm
# robot.move_to_position(target_position)
# print(f"Current position after movement: {robot.current_position}")

