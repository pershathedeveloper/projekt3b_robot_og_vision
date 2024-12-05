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

class ObjectDetector:
    def __init__(self, lower_color1, upper_color1, lower_color2=None, upper_color2=None, color_name=""):
        self.lower_color1 = lower_color1
        self.upper_color1 = upper_color1
        self.lower_color2 = lower_color2
        self.upper_color2 = upper_color2
        self.color_name = color_name

    def detect_object(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, self.lower_color1, self.upper_color1)
        if self.lower_color2 is not None and self.upper_color2 is not None:
            mask2 = cv2.inRange(hsv, self.lower_color2, self.upper_color2)
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            mask = mask1

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detected_objects = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 500:  # Filtrer meget små objekter
                continue

            x, y, w, h = cv2.boundingRect(contour)
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) >= 8:  # Hvis konturen har mange hjørner, er det sandsynligvis en cirkel
                shape = "circle"
            else:
                shape = "square"

            detected_objects.append((shape, x, y, w, h, self.color_name))
        return detected_objects

# Pipeline og enhedsopsætning
pipeline = dai.Pipeline()
cam_rgb = pipeline.createColorCamera()
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam_rgb.setPreviewSize(1280, 720)
cam_rgb.setInterleaved(False)
xout_video = pipeline.createXLinkOut()
xout_video.setStreamName("video")
cam_rgb.preview.link(xout_video.input)

with dai.Device(pipeline) as device:
    video_queue = device.getOutputQueue(name="video", maxSize=1, blocking=False)

    detector_red = ObjectDetector(base_lower_red1, base_upper_red1, base_lower_red2, base_upper_red2, "red")
    detector_green = ObjectDetector(base_lower_green, base_upper_green, color_name="green")

    print("Tryk på 'q' for at afslutte.")

    while True:
        frame = video_queue.get().getCvFrame()

        # Detekter røde objekter
        detected_objects_red = detector_red.detect_object(frame)
        for obj in detected_objects_red:
            shape, x, y, w, h, color = obj
            if shape == "square":
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            elif shape == "circle":
                cv2.circle(frame, (x + w // 2, y + h // 2), w // 2, (0, 0, 255), 2)
            cv2.putText(frame, f"{color} {shape}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Detekter grønne objekter
        detected_objects_green = detector_green.detect_object(frame)
        for obj in detected_objects_green:
            shape, x, y, w, h, color = obj
            if shape == "square":
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            elif shape == "circle":
                cv2.circle(frame, (x + w // 2, y + h // 2), w // 2, (0, 255, 0), 2)
            cv2.putText(frame, f"{color} {shape}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()