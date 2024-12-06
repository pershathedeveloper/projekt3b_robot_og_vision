import depthai as dai
import cv2
import numpy as np
import rtde_control
import rtde_receive

# Grundlæggende HSV-værdier for farver
base_lower_red1 = np.array([0, 100, 50])  # Rød farve lav grænse 1
base_upper_red1 = np.array([10, 255, 255])
base_lower_red2 = np.array([160, 100, 50])
base_upper_red2 = np.array([180, 255, 255])

base_lower_green = np.array([35, 100, 50])  # Grøn farve grænser
base_upper_green = np.array([85, 255, 255])

# RTDE-opsætning til robotkontrol
ur_robot_ip = "192.168.0.51"  # Din UR-robot IP-adresse
rtde_c = rtde_control.RTDEControlInterface(ur_robot_ip)

# Kamera- og robotkalibreringspunkter
camera_points = np.array([
    [100, 700],   # Venstre nederste hjørne
    [100, 100],   # Venstre øverste hjørne
    [1100, 700],  # Højre nederste hjørne
    [1100, 100],  # Højre øverste hjørne
], dtype=np.float32)

robot_points = np.array([
    [-441.79, 278.26, -344.37],  # Venstre nederste hjørne
    [-477.21, -51.24, -344.47],  # Venstre øverste hjørne
    [-222.63, 285.52, -346.03],  # Højre nederste hjørne
    [-227.94, -73.51, -344.42],  # Højre øverste hjørne
], dtype=np.float32)

robot_points_2d = robot_points[:, :2]
homography_matrix, _ = cv2.findHomography(camera_points, robot_points_2d)

# Funktion til at konvertere pixel til robotkoordinater
def pixel_to_robot(u, v, homography_matrix, z_robot=-0.344):
    pixel_point = np.array([u, v, 1], dtype=np.float32).reshape(-1, 1)
    robot_point = np.dot(homography_matrix, pixel_point)
    robot_point /= robot_point[2]  # Normaliser
    return robot_point[0], robot_point[1], z_robot

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

# Objekt detektor klasse
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

# Pipeline og enhedsopsætning
camera = OakDCamera()
detector_red = ObjectDetector(base_lower_red1, base_upper_red1, base_lower_red2, base_upper_red2, "red")
detector_green = ObjectDetector(base_lower_green, base_upper_green, color_name="green")

print("Tryk på 'q' for at afslutte.")

while True:
    frame = camera.get_frame()

    # Detekter røde objekter
    detected_objects_red = detector_red.detect_object(frame)
    for obj in detected_objects_red:
        x, y, w, h, color = obj
        cv2.circle(frame, (x + w // 2, y + h // 2), w // 2, (0, 0, 255), 2)
        cv2.putText(frame, f"{color} circle ({x}, {y})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Konverter pixelkoordinater til robotkoordinater
        robot_x, robot_y, robot_z = pixel_to_robot(x + w // 2, y + h // 2, homography_matrix)
        print(f"Flytter robot til: X={robot_x}, Y={robot_y}, Z={robot_z}")
        rtde_c.moveL([robot_x, robot_y, robot_z, 0, 0, 0])

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
