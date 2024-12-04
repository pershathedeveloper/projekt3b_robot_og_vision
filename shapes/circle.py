from shapes.shape import Shape

class Circle(Shape):
    def __init__(self, radius=0.0, position=None):
        super().__init__("Circle", position)
        self.radius = radius

    def calculateArea(self):
        return 3.14159 * (self.radius ** 2)
