
import cv2
import depthai as dai

# Opret et pipeline-objekt
pipeline = dai.Pipeline()

# Opret en farve (RGB) kamera-node
color_cam = pipeline.createColorCamera()
color_cam.setPreviewSize(640, 480)  # Sæt preview-opløsning
color_cam.setInterleaved(False)     # Brug planer RGB-format
color_cam.setFps(30)                # FPS for videostream

# Opret en XLink output-node til at sende videostreamen
xout = pipeline.createXLinkOut()
xout.setStreamName("video")
color_cam.preview.link(xout.input)

# Start pipeline og forbind til kameraet
with dai.Device(pipeline) as device:
    print("OAK-D kamera tilsluttet!")

    # Få adgang til videostream
    video_queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    while True:
        # Hent næste frame fra videostream
        in_video = video_queue.get()
        frame = in_video.getCvFrame()  # Konverter til OpenCV format

        # Vis billedet i et vindue
        cv2.imshow("OAK-D Live Stream", frame)

        # Afslut med 'q'-tasten
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Luk vinduet
cv2.destroyAllWindows()
