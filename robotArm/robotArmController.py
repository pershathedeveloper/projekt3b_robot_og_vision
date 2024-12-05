from robotArm.robotArmKinematics import RobotArmKinematics
from robotArm.robotArmRTDE import RobotArmRTDE

class RobotArmController:
    def __init__(self):
        self.robotArm = RobotArmKinematics()
        self.rtde = RobotArmRTDE()

    def moveToPosition(self, position):
        path = self.robotArm.calculatePath(position)
        for waypoint in path.waypoints:
            print(f"Moving to {waypoint}")
        self.robotArm.updatePosition(position)

    def gripObject(self):
        self.rtde.sendCommand("set_digital_out(8, True)")
        print("Gripping object...")

    def releaseObject(self):
        self.rtde.sendCommand("set_digital_out(8, False)")
        print("Releasing object...")

    def closeConnection(self):
        self.rtde.close()
        print("Connection closed.")
