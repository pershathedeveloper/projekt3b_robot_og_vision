import unittest
from vision.visionCameraController import VisionCameraController
from vision.visionImageProcessor import VisionImageProcessor
from vision.visionObjectDetector import VisionObjectDetector
from unittest.mock import MagicMock

class TestVisionCameraController(unittest.TestCase):

    def test_open_pipeline(self):
        # Create mock instance
        camera = VisionCameraController()
        camera.device = MagicMock()  # Mock device object
        
        # Call openPipeline
        camera.openPipeline()
        
        # Assert that device initialization is called
        camera.device.__enter__.assert_called_once()

    def test_capture_image(self):
        # Create mock instance
        camera = VisionCameraController()
        camera.device = MagicMock()
        camera.device.getOutputQueue = MagicMock(return_value=MagicMock())  # Mock queue
        
        # Capture image
        frame = camera.captureImage()
        
        # Assert that getOutputQueue was called
        camera.device.getOutputQueue.assert_called_once()
        self.assertIsNotNone(frame)  # Ensure frame is not None

class TestVisionImageProcessor(unittest.TestCase):

    def test_process_image(self):
        # Create mock instance
        processor = VisionImageProcessor(algorithm="default")
        
        # Test image processing
        processed_data = processor.processImage("dummy_image")
        
        # Assert that processed data is returned
        self.assertEqual(processed_data, {"processedData": "some_data"})

class TestVisionObjectDetector(unittest.TestCase):

    def test_detect_objects(self):
        # Create mock instance
        detector = VisionObjectDetector(detectionThreshold=0.5)
        
        # Test object detection
        detected_objects = detector.detectObjects({"processedData": "some_data"})
        
        # Assert that detected objects are returned
        self.assertEqual(detected_objects, ["Object1", "Object2"])

if __name__ == "__main__":
    unittest.main()
