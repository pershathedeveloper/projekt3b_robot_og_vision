from vision.visionCameraController import VisionCameraController
from vision.visionObjectDetector import VisionObjectDetector
from robotArm.robotArmController import RobotArmController
from utils.dataUtils import DataUtils
from vision.visionImageProcessor import VisionImageProcessor

def main():
    # Initialize system components
    camera = VisionCameraController()
    processor = VisionImageProcessor()
    detector = VisionObjectDetector()
    robotArm = RobotArmController()

    # Capture an image
    camera.openPipeline()
    image = camera.captureImage()

    # Process the image
    processedData = processor.processImage(image)

    # Detect objects (optional)
    detectedObjects = detector.detectObjects(processedData)

    # Instruct the robot arm
    robotArm.moveToPosition((0.5, 0.2, 0.3))  # Example position
    robotArm.gripObject()
    robotArm.releaseObject()

    # Save results
    DataUtils.saveData(processedData, "output.dat")

    # Clean up
    camera.close()
    robotArm.closeConnection()

if __name__ == "__main__":
    main()