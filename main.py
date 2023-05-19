import mindstorms
import numpy as np

class GantryRobot:
    def __init__(self, gear_ratio):
        """
            @param gear_ratio: gear ratio for rack and pinion
        """
        self.gear_ratio = gear_ratio  # gear ratio for rack and pinion
        self.motor_resolution = 360  # degrees of rotation for one full rotation of the motor
        self.cm_per_rotation = 1  # cm moved per full rotation of the gear

    
    def motor_to_cm(self, motor_rotation):
        """
            Converts number of motor rotations to lateral cm moved

            @param motor_rotation: number of motor rotations
            @return distance_moved: distance moved in cm
        """
        gear_rotation = motor_rotation / self.gear_ratio
        distance_moved = gear_rotation * self.cm_per_rotation
        return distance_moved

    # cm to motor and motor to cm conversions
    def cm_to_motor(self, distance_cm):
        """
            Converts lateral cm moved to number of motor rotations

            @param distance_cm: distance in cm
            @return motor_rotation: motor rotation needed to move distance_cm
        """
        gear_rotation = distance_cm / self.cm_per_rotation
        motor_rotation = gear_rotation * self.gear_ratio
        return motor_rotation

    def forward_kinematics(self, motor_rotations):
        """
            Calculates forward kinematics
            
            @param motor_rotations: number of motor rotations for each motor
        """
        # calculate forward kinematics
        x, y, z = motor_rotations
        x_cm = self.motor_to_cm(x)
        y_cm = self.motor_to_cm(y)
        z_cm = self.motor_to_cm(z)
        return np.array([x_cm, y_cm, z_cm])

    def inverse_kinematics(self, target_position):
        # calculate inverse kinematics
        x_cm, y_cm, z_cm = target_position
        x_motor = self.cm_to_motor(x_cm)
        y_motor = self.cm_to_motor(y_cm)
        z_motor = self.cm_to_motor(z_cm)
        return np.array([x_motor, y_motor, z_motor])


# Example usage
robot = GantryRobot(gear_ratio=1)  # adjust gear_ratio as needed
target_position = np.array([10, 20, 30])  # target position in cm
motor_rotations = robot.inverse_kinematics(target_position)
print(f"Motor rotations needed: {motor_rotations}")
