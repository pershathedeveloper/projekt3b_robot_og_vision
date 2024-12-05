class Shape:
    def __init__(self, type="undefined", position=None):
        self.type = type
        self.position = position if position else Position(0, 0, 0)

    def calculateArea(self):
        raise NotImplementedError("This method must be implemented by subclasses.")
