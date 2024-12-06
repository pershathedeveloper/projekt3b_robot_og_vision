import rtde_control
import rtde_receive
import depthai as dai
import numpy as np
import time

# Robot IP-adresse
ROBOT_HOST = "192.168.0.51"  # Erstat med robotarmens IP-adresse

# Initialiser RTDE Control og Receive
rtde_c = rtde_control.RTDEControlInterface(ROBOT_HOST)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_HOST)

# Definer ROI (Region of Interest) i pixels
ROI_min_x = 200
ROI_max_x = 300
ROI_min_y = 100
ROI_max_y = 200

# OAK-D pipeline opsætning
def create_pipeline():
    pipeline = dai.Pipeline()

    # Opret RGB-kamera
    cam_rgb = pipeline.createColorCamera()
    cam_rgb.setPreviewSize(640, 480)
    cam_rgb.setInterleaved(False)
    cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)

    # Opret dybdekort
    mono_left = pipeline.createMonoCamera()
    mono_right = pipeline.createMonoCamera()
    stereo = pipeline.createStereoDepth()

    mono_left.setBoardSocket(dai.CameraBoardSocket.LEFT)
    mono_right.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)

    # Link dybdeoutput til pipeline
    xout_rgb = pipeline.createXLinkOut()
    xout_rgb.setStreamName("rgb")
    cam_rgb.preview.link(xout_rgb.input)

    xout_depth = pipeline.createXLinkOut()
    xout_depth.setStreamName("depth")
    stereo.depth.link(xout_depth.input)

    return pipeline

# OAK-D og RTDE-integration
pipeline = create_pipeline()
with dai.Device(pipeline) as device:
    rgb_queue = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    depth_queue = device.getOutputQueue(name="depth", maxSize=4, blocking=False)

    while True:
        # Få RGB og dybdekort
        rgb_frame = rgb_queue.get().getCvFrame()
        depth_frame = depth_queue.get().getFrame()

        # Simuleret pixelkoordinater (erstat med faktisk AI eller OpenCV-finding)
        pixel_x, pixel_y = 250, 150
        depth_z = depth_frame[pixel_y, pixel_x] / 1000.0  # Konverter dybde fra mm til meter

        # Tjek om objektet er inden for ROI
        if ROI_min_x <= pixel_x <= ROI_max_x and ROI_min_y <= pixel_y <= ROI_max_y:
            print("Objekt inden for ROI. Flytter robot...")

            # Konverter pixelkoordinater til verdenskoordinater
            scale_factor = 0.001  # Skaler pixel til meter (afhængig af kameraets opsætning)
            world_x = pixel_x * scale_factor
            world_y = pixel_y * scale_factor
            world_z = depth_z

            # Robotens målposition
            target_pose = [world_x, world_y, world_z, 0, 3.14, 0]  # Orientering kan justeres
            rtde_c.moveL(target_pose, acceleration=0.5, velocity=0.2)
        else:
            print("Objekt uden for ROI. Ingen bevægelse.")

        time.sleep(0.5)  # Loop-interval