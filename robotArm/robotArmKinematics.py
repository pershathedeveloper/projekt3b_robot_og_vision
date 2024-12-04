class RobotArmKinematics:
    def __init__(self):
        self.currentPosition = (0, 0, 0)

    def calculatePath(self, target_position):
        path = Path([self.currentPosition, target_position])
        return path

    def updatePosition(self, target_position):
        self.currentPosition = target_position
        print(f"Updated position to {self.currentPosition}")
