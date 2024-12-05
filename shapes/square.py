from shapes.shape import Shape

class Square(Shape):
    def __init__(self, sideLength=0.0, position=None):
        super().__init__("Square", position)
        self.sideLength = sideLength

    def calculateArea(self):
        return self.sideLength ** 2
