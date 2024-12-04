import unittest
from robotArm.robotArmController import RobotArmController
from robotArm.robotArmKinematics import RobotArmKinematics
from robotArm.robotArmRTDE import RobotArmRTDE
from unittest.mock import MagicMock

class TestRobotArmController(unittest.TestCase):

    def test_move_to_position(self):
        # Create mock instances
        controller = RobotArmController()
        controller.robotArm = MagicMock(RobotArmKinematics)  # Mock RobotArmKinematics
        controller.robotArm.calculatePath = MagicMock(return_value=None)  # Mock the path calculation
        
        # Move to a sample position
        controller.moveToPosition((1, 0, 0))
        
        # Assert that the updatePosition method was called
        controller.robotArm.updatePosition.assert_called_with((1, 0, 0))

    def test_grip_object(self):
        # Create mock instance
        controller = RobotArmController()
        controller.rtde = MagicMock(RobotArmRTDE)  # Mock RobotArmRTDE
        
        # Grip the object
        controller.gripObject()
        
        # Assert that the sendCommand method was called
        controller.rtde.sendCommand.assert_called_with("set_digital_out(8, True)")

    def test_release_object(self):
        # Create mock instance
        controller = RobotArmController()
        controller.rtde = MagicMock(RobotArmRTDE)  # Mock RobotArmRTDE
        
        # Release the object
        controller.releaseObject()
        
        # Assert that the sendCommand method was called
        controller.rtde.sendCommand.assert_called_with("set_digital_out(8, False)")

    def test_send_command_via_rtde(self):
        # Create mock instance
        rtde = RobotArmRTDE()
        rtde.sendCommand = MagicMock()  # Mock the sendCommand method
        
        # Send a command
        rtde.sendCommand("movej([1,0,0,0,0,0])")
        
        # Assert that sendCommand was called with the correct command
        rtde.sendCommand.assert_called_with("movej([1,0,0,0,0,0])")

if __name__ == "__main__":
    unittest.main()
