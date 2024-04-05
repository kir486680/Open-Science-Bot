import numpy as np
from mindstorms import Motor, Hub
import time
from typing import Union
import json
from pathlib import Path

state_path = Path(__file__).parent / "state/state.json"

class Gantry:
    def __init__(self, gear_ratios=[1, 1, 1,1], motor_resolution=360):
        self.gear_ratios = np.array(
            gear_ratios
        )  # gear ratios for rack and pinion in X, Y, Z
        self.motor_resolution = (
            motor_resolution  # degrees of rotation for one full rotation of the motor
        )
        self.cm_per_rotation = np.array(
            [1, 1, 1,1]
        )  # cm moved per full rotation of the gear in X, Y, Z
        self.current_position = np.array(
            [0, 0, 0,0]
        )  # current position of the robot in cm
        self.hub = None
        try:
            self.hub = Hub()
            time.sleep(1)
            self.motors = [
                self.hub.port.A.motor,
                self.hub.port.B.motor,
                self.hub.port.D.motor,
                self.hub.port.E.motor,
            ]  # adjust motor ports as needed
        except:
            print("No hub found, No motors initialized")

        # Load the state from the JSON file
        with open(state_path, "r") as f:
            state = json.load(f)
            self.current_position = np.array([state["x"], state["y"], state["z"], state["z1"]])
            # print (f"Current position: {self.current_position}")
            # Move the gantry to the loaded state
            self.move_to_position(self.current_position)

    def set_cm_per_rotation(self, cm_per_rotation: Union[list, np.ndarray]) -> None:
        """
        Set the cm per rotation for the robot

        Args:
            cm_per_rotation (Union[list, np.ndarray]): list of cm per rotation for each axis

        Raises:
            ValueError: If cm_per_rotation is not of length 3, or contains non-numeric values.

        Returns:
            None
        """
        if len(cm_per_rotation) != 4:
            raise ValueError("cm_per_rotation must contain exactly 3 elements")

        if not all(isinstance(x, (int, float)) for x in cm_per_rotation):
            raise ValueError("All elements of cm_per_rotation must be numeric")

        self.cm_per_rotation = np.array(cm_per_rotation)

    def motor_to_cm(self, motor_rotations: Union[list, np.ndarray]):
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

    def cm_to_motor(self, distances_cm: Union[list, np.ndarray]):
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

    def forward_kinematics(
        self, motor_rotations: Union[list, np.ndarray]
    ) -> Union[list, np.ndarray]:
        """
        Calculate forward kinematics

        Args:
            motor_rotations (array): array of motor rotations for each axis

        Returns:
            current_position (array): array of current position for each axis
        """
        self.current_position = self.motor_to_cm(motor_rotations)
        return self.current_position

    def inverse_kinematics(
        self, target_position: Union[list, np.ndarray]
    ) -> Union[list, np.ndarray]:
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

    def move_to_position(self, target_position: Union[list, np.ndarray]) -> None:
        """
        Move the robot to the target position

        Args:
            target_position (Union[list, np.ndarray]): array of target position for each axis

        Raises:
            ValueError: If target_position is not of length 4, contains non-numeric values, or is out of bounds.

        Returns:
            None
        """

        if len(target_position) != 4:
            print(target_position)
            raise ValueError("target_position must contain exactly 4 elements")
        
        if target_position[2] > 0:
            target_position[2]= - target_position[2] #due to the fact that the motors are inverted. Ugly solution, but it works

        """ if not all(isinstance(x, (int, float)) for x in target_position):
            raise ValueError("All elements of target_position must be numeric")  """

        min_x, min_y, min_z, min_z1,max_x, max_y, max_z,max_z1 = (
            0,
            0,
            -4.5,
            -4.5,
            40,
            20,
            4.5,
            4.5,
        )  
        if target_position[0] < min_x or target_position[0] > max_x:
            raise ValueError(f"X must be between {min_x} and {max_x}")
        if target_position[1] < min_y or target_position[1] > max_y:
            raise ValueError(f"Y must be between {min_y} and {max_y}")
        if target_position[2] < min_z or target_position[2] > max_z:
            raise ValueError(f"Z must be between {min_z} and {max_z}")
        if target_position[3] < min_z1 or target_position[2] > max_z1:
            raise ValueError(f"Z must be between {min_z1} and {max_z1}")
        
        if self.hub != None:
            # move motors to target position
            motor_rotations = self.inverse_kinematics(target_position)
            print(f"Motor rotations: {motor_rotations}")
            for motor, rotation in zip(self.motors, motor_rotations):
                print(f"Motor: {motor}, rotation: {rotation}")
                rotation_degrees = (
                    rotation * self.motor_resolution
                )  # convert rotations to degrees
                print(f"Rotation degrees: {rotation_degrees}")
                if rotation_degrees >= 0:
                    # pass
                    motor.run_for_degrees(abs(rotation_degrees), speed=-60)
                else:
                    motor.run_for_degrees(abs(rotation_degrees), speed=60)
                time.sleep(0.1)

        # Update the current positions:
        self.current_position = target_position

        # Update the state in the JSON file
        with open(state_path, "r") as f:
            state = json.load(f)

        state["x"] = float(self.current_position[0])
        state["y"] = float(self.current_position[1])
        state["z"] = float(self.current_position[2])
        state["z1"] = float(self.current_position[3])


        with open(state_path, "w") as f:
            json.dump(state, f, indent=4)


# Example usage
# robot = Gantry(gear_ratios=[1, 1, 1])  # adjust gear_ratios as needed
# robot.set_cm_per_rotation([4, 12.56, 1])  # adjust cm_per_rotation as needed
# target_position = np.array([20, 20, 0])  # target position in cm
# robot.move_to_position(target_position)
# print(f"Current position after movement: {robot.current_position}")
