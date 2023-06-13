try:
    import picamera
except (ImportError, ValueError):
    # We're not on a Raspberry Pi - use a mock camera
    class MockCamera:
        def __init__(self):
            print("Initialising camera mock")
        
        def start_preview(self):
            print("Starting preview mock")

        def stop_preview(self):
            print("Stopping preview mock")

        # Add more methods as needed based on what you use from picamera.
    
    picamera = MockCamera

import time
import cv2
import numpy as np
import io


class Camera:
    def __init__(self, camera_type="pi"):
        """Camera constructor. Creates different types of camera objects depending on the type.

        Args:
            camera_type (str): Type of camera. Either "pi" for Raspberry Pi camera or "usb" for USB camera.
        """
        if camera_type == "pi":
            self.camera = picamera.PiCamera()
            time.sleep(2)
        elif camera_type == "usb":
            self.camera = cv2.VideoCapture(1)  # Update the camera index as needed
        self.camera_type = camera_type

    def __del__(self):
        """Destructor for usb camera case, where opencv needs to release system resources."""

        if self.camera_type == "usb":
            self.camera.release()

    def get_image(self):
        """Gets a singular image frame from the camera and returns a numpy array representing the pixels of the image.

        Returns:
            np.ndarray: Numpy array representing the image frame.
        """

        if self.camera_type == "pi":
            # Capture image using picamera and return it as numpy array
            stream = io.BytesIO()
            self.camera.capture(stream, format="jpeg")
            stream.seek(0)
            image = np.frombuffer(stream.getvalue(), dtype=np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            return image
        elif self.camera_type == "usb":
            # Capture frame using OpenCV
            ret, frame = self.camera.read()
            return frame

    def preview_camera(self):
        """Previews the camera for a few seconds, or until the user presses the q key."""

        if self.camera_type == "pi":
            self.camera.start_preview()
            time.sleep(15)  # Preview for 15 seconds
            self.camera.stop_preview()
        elif self.camera_type == "usb":
            # Define the desired window dimensions
            window_width = 640
            window_height = 480

            # Set the window size
            cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Camera", window_width, window_height)

            while True:  # Preview until q key is pressed
                ret, frame = self.camera.read()

                # Resize the frame to the desired dimensions
                frame = cv2.resize(frame, (window_width, window_height))

                # Display the resized frame
                cv2.imshow("Camera", frame)

                if cv2.waitKey(1) == ord("q"):
                    break

            cv2.destroyAllWindows()

    def segment_image(self, image):
        """Calls the segmentation algorithm.

        Args:
            image (np.ndarray): Input image for segmentation.

        Returns:
            np.ndarray: Segmented image.
        """
        # TODO: Implement the segmentation algorithm on the input image and return the segmented image
        return None

    def label_image(self, image):
        """Calls the labeling algorithm.

        Args:
            image (np.ndarray): Input image for labeling.

        Returns:
            np.ndarray: Labeled image.
        """
        # TODO: Implement the labeling algorithm on the input image and return the labeled image
        return None
