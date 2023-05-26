import unittest
import numpy as np
from lego_brain import Gantry  # assuming the GantryRobot class is in a file named gantry_robot.py

class TestGantryRobot(unittest.TestCase):
    def setUp(self):
        self.robot = Gantry(gear_ratios=[1, 1, 1])
        self.robot.set_cm_per_rotation([4, 4, 1])

    def test_motor_to_cm(self):
        motor_rotations = np.array([1, 2, 3])
        expected_result = motor_rotations * self.robot.cm_per_rotation
        np.testing.assert_array_equal(self.robot.motor_to_cm(motor_rotations), expected_result)

    def test_cm_to_motor(self):
        distances_cm = np.array([4, 8, 12])
        expected_result = distances_cm / self.robot.cm_per_rotation
        np.testing.assert_array_equal(self.robot.cm_to_motor(distances_cm), expected_result)

    def test_forward_kinematics(self):
        motor_rotations = np.array([1, 2, 3])
        expected_result = self.robot.motor_to_cm(motor_rotations)
        np.testing.assert_array_equal(self.robot.forward_kinematics(motor_rotations), expected_result)

    def test_inverse_kinematics(self):
        target_position = np.array([30, 20, 30])
        expected_result = self.robot.cm_to_motor(target_position - self.robot.current_position)
        np.testing.assert_array_equal(self.robot.inverse_kinematics(target_position), expected_result)

    # def test_move_to_position(self):
    #     target_position = np.array([30, 20, 30])
    #     expected_result = self.robot.cm_to_motor(target_position - self.robot.current_position)
    #     self.robot.move_to_position(target_position)
    #     np.testing.assert_array_equal(self.robot.current_position, target_position)

if __name__ == '__main__':
    unittest.main()
