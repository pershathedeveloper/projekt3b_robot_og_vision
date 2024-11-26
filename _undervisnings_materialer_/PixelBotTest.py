from PixelBot import PixelBot
import cv2

bot = PixelBot()
bot.startPixelBot()

for i in range(50):
    bot.setPos(i,i)
    cv2.waitKey(100)