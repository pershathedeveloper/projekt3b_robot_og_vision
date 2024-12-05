class Position:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def calculateDistance(self, pos2):
        return ((self.x - pos2.x) ** 2 + (self.y - pos2.y) ** 2 + (self.z - pos2.z) ** 2) ** 0.5
