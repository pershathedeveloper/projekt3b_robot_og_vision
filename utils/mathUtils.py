class MathUtils:
    @staticmethod
    def calculateDistance(pos1, pos2):
        return ((pos2.x - pos1.x) ** 2 + (pos2.y - pos1.y) ** 2 + (pos2.z - pos1.z) ** 2) ** 0.5

    @staticmethod
    def calculateArea(radius):
        return 3.14159 * radius ** 2

    @staticmethod
    def calculateSquareArea(sideLength):
        return sideLength ** 2
