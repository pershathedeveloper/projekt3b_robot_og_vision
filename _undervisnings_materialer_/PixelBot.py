import cv2
import numpy as np

class PixelBot:

    def __init__(self, x: int = 64, y: int = 64, windowScale: float = 8) -> None:
        self.map = np.zeros([x,y,1], dtype=np.uint8)
        self.pos = [0, 0]
        self.map.fill(255)
        cv2.namedWindow("PixelBot", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("PixelBot", x * windowScale, y * windowScale)

    def startPixelBot(self, x:int = 0, y: int = 0):
        self.pos = [x, y]
        self.setPos(self.pos[0], self.pos[1])

    def setPos(self, x:int, y:int):
        self.map[self.pos[0], self.pos[1]] = 255
        self.pos = [x, y]
        self.map[self.pos[0], self.pos[1]] = 0
        cv2.imshow("PixelBot", self.map)