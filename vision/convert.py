import depthai as dai
import cv2
import numpy as np
import rtde_control
import rtde_receive

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
                detected_objects.append((x, y, w, h, self.color_name))
        return detected_objects

# RTDE setup
ur_robot_ip = "192.168.0.51"  # Skift til UR-robotens IP-adresse
rtde_c = rtde_control.RTDEControlInterface(ur_robot_ip)
rtde_r = rtde_receive.RTDEReceiveInterface(ur_robot_ip)

# Kalibreringsfunktion (skal tilpasses din opsætning)
def convert_to_robot_coordinates(x, y, w, h):
    # Eksempel på en simpel lineær transformation
    # Disse værdier skal tilpasses baseret på din kalibrering
    scale_x = 0.001  # Skaleringsfaktor for x-aksen
    scale_y = 0.001  # Skaleringsfaktor for y-aksen
    offset_x = 0.5   # Offset for x-aksen
    offset_y = 0.5   # Offset for y-aksen

    robot_x = x * scale_x + offset_x
    robot_y = y * scale_y + offset_y
    robot_z = 0.1  # Eksempel på en fast z-koordinat
    return robot_x, robot_y, robot_z

# Konverter robotkoordinater til radianer (eksempel)
def convert_to_radians(x, y, z):
    # Konvertering til radianer afhænger af din opsætning og robotens arbejdsområde
    # Her er et eksempel på en simpel konvertering
    rad_x = np.deg2rad(x)
    rad_y = np.deg2rad(y)
    rad_z = np.deg2rad(z)
    return rad_x, rad_y, rad_z

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
            x, y, w, h, color = obj
            cv2.circle(frame, (x + w // 2, y + h // 2), w // 2, (0, 0, 255), 2)
            cv2.putText(frame, f"{color} circle ({x}, {y})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Konverter billedkoordinater til robotkoordinater
            robot_x, robot_y, robot_z = convert_to_robot_coordinates(x + w // 2, y + h // 2, w, h)
            print(f"Detected object at image coordinates: x={x + w // 2}, y={y + h // 2}")
            print(f"Converted to robot coordinates: x={robot_x}, y={robot_y}, z={robot_z}")

            # Konverter robotkoordinater til radianer
            rad_x, rad_y, rad_z = convert_to_radians(robot_x, robot_y, robot_z)
            print(f"Converted to radians: x={rad_x}, y={rad_y}, z={rad_z}")

            # Send koordinater til robotten
            rtde_c.moveL([rad_x, rad_y, rad_z, 0, 0, 0], speed=0.1, acceleration=0.1)

        # Detekter grønne objekter
        detected_objects_green = detector_green.detect_object(frame)
        for obj in detected_objects_green:
            x, y, w, h, color = obj
            cv2.circle(frame, (x + w // 2, y + h // 2), w // 2, (0, 255, 0), 2)
            cv2.putText(frame, f"{color} circle ({x}, {y})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    rtde_c.stopScript()