import depthai as dai

class VisionCameraController:
    def __init__(self):
        self.pipeline = dai.Pipeline()
        self.device = None

    def openPipeline(self):
        self.device = dai.Device(self.pipeline)
        print("Camera pipeline opened.")

    def captureImage(self):
        if not self.device:
            raise Exception("Pipeline not opened.")
        frame = self.device.getOutputQueue(name="video", maxSize=4, blocking=False).get().getCvFrame()
        return frame

    def close(self):
        self.device = None
        print("Camera pipeline closed.")
