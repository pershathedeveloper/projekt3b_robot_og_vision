import math

class Shape:
    def __init__(self, name) -> None:
        self.name = name

    def printName(self):
        print(self.name)

    def getArea():
        return 0

class Firkant(Shape):
    def __init__(self, iLenght, iHeight):
        Shape.__init__(self, 'firkant')
        self.lenght = iLenght
        self.heigth = iHeight

    def getArea(self):
        return self.heigth * self.lenght

class Cirkel(Shape):
    def __init__(self, r):
        Shape.__init__(self, 'cirkel')
        self.r = r

    def getArea(self):
        return self.r * self.r * math.pi
    
class Trekant(Shape):
    def __init__(self, l, h) -> None:
        super().__init__('trekant')
        self.l = l
        self.h = h
    
    def getArea(self):
        return self.l * self.h * 0.5
    

def sumAreaShapes(shape1:Shape, shape2:Shape):
    return shape1.getArea() + shape2.getArea()

myFirkant = Firkant(2, 4)
myFirkant.printName()
myCirkel = Cirkel(2)
myCirkel.printName()
myTrekant = Trekant(2, 4)
myTrekant.printName()
print("firkant_area:", myFirkant.getArea())
print("cirkel_area:", myCirkel.getArea())
print("sum_area", sumAreaShapes(myFirkant, myTrekant))