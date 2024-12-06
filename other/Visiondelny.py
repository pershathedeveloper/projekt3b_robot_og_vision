import depthai as dai
import cv2
import numpy as np

# Grundlæggende HSV-værdier for farver
base_lower_red1 = np.array([0, 100, 50])  # Grundværdier for rød
base_upper_red1 = np.array([10, 255, 255])
base_lower_red2 = np.array([160, 100, 50])
base_upper_red2 = np.array([180, 255, 255])

base_lower_green = np.array([35, 100, 50])  # Grundværdier for grøn
base_upper_green = np.array([85, 255, 255])

# Oak-D kamera klasse
class OakDCamera:
    def __init__(self):
        self.pipeline = dai.Pipeline()
        self.cam_rgb = self.pipeline.createColorCamera()
        self.cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        self.cam_rgb.setPreviewSize(1280, 720)
        self.cam_rgb.setInterleaved(False)
        self.xout_video = self.pipeline.createXLinkOut()
        self.xout_video.setStreamName("video")
        self.cam_rgb.preview.link(self.xout_video.input)
        self.device = dai.Device(self.pipeline)
        self.video = self.device.getOutputQueue(name="video", maxSize=4, blocking=False)

    def get_frame(self):
        in_video = self.video.get()
        frame = in_video.getCvFrame()
        return frame

    def take_picture(self, filename):
        frame = self.get_frame()
        cv2.imwrite(filename, frame)
        print(f"Billede gemt som {filename}")

    def stream_video(self):
        while True:
            frame = self.get_frame()
            cv2.imshow("Video Stream", frame)

            # Tryk på 'q' for at afslutte streamen
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

class ObjectDetector:
    def __init__(self, colors):
        self.colors = colors

    def detect_objects(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        detected_objects = []

        for color in self.colors:
            lower_color1, upper_color1, lower_color2, upper_color2, color_name = color
            mask1 = cv2.inRange(hsv, lower_color1, upper_color1)
            mask2 = cv2.inRange(hsv, lower_color2, upper_color2)
            mask = cv2.bitwise_or(mask1, mask2)

            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 500:  # Filtrer meget små objekter
                    continue

                x, y, w, h = cv2.boundingRect(contour)
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                if len(approx) >= 8:  # Hvis konturen har mange hjørner, er det sandsynligvis en cirkel
                    shape = "circle"
                    detected_objects.append((shape, x, y, w, h, color_name, x + w // 2, y + h // 2))

        return detected_objects

# Brug kameraet til at streame video og identificere objekter
if __name__ == "__main__":
    camera = OakDCamera()
    colors = [
        (base_lower_red1, base_upper_red1, base_lower_red2, base_upper_red2, "red"),
        (base_lower_green, base_upper_green, base_lower_green, base_upper_green, "green")
    ]
    detector = ObjectDetector(colors)

    while True:
        frame = camera.get_frame()
        detected_objects = detector.detect_objects(frame)

        for obj in detected_objects:
            shape, x, y, w, h, color, center_x, center_y = obj
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{shape} ({color})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(frame, f"({center_x}, {center_y})", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Video Stream", frame)

        # Tryk på 'q' for at afslutte streamen
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()