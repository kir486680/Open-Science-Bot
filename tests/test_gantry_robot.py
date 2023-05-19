import unittest
import numpy as np
from main import GantryRobot  # assuming the GantryRobot class is in a file named gantry_robot.py

class TestGantryRobot(unittest.TestCase):
    def setUp(self):
        self.robot = GantryRobot(gear_ratio=1)

    def test_forward_kinematics(self):
        motor_rotations = np.array([360, 720, 1080])
        expected_position = np.array([1, 2, 3])
        np.testing.assert_array_equal(self.robot.forward_kinematics(motor_rotations), expected_position)

    def test_inverse_kinematics(self):
        target_position = np.array([1, 2, 3])
        expected_rotations = np.array([360, 720, 1080])
        np.testing.assert_array_equal(self.robot.inverse_kinematics(target_position), expected_rotations)

    def test_edge_case_zero(self):
        # test edge case where target position is zero
        target_position = np.array([0, 0, 0])
        expected_rotations = np.array([0, 0, 0])
        np.testing.assert_array_equal(self.robot.inverse_kinematics(target_position), expected_rotations)

    def test_edge_case_max(self):
        # test edge case where target position is at maximum possible value
        target_position = np.array([1000, 1000, 1000])  # adjust as needed
        expected_rotations = target_position * 360  # adjust as needed
        np.testing.assert_array_equal(self.robot.inverse_kinematics(target_position), expected_rotations)

if __name__ == '__main__':
    unittest.main()
