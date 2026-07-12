import sys

import cv2
import numpy as np

import logger

awcr_logger = logger.get_logger(__name__)

CAMERA_WIDTH = 900
CAMERA_HEIGHT = 650
FPS_VALUE = 25


class CameraService:
    """
    Manages the camera capture device: opening, configuration, frame reading and releasing.
    """
    def __init__(self):
        self.camera = None

    def open_camera(self) -> bool:
        """
        Opens the camera and configures its resolution and frame rate.

        Returns:
            bool: True if the camera was opened successfully, False otherwise.
        """
        if sys.platform == "win32":
            self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        else:
            self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            awcr_logger.error("Error! Can't open the camera!")
            return False

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        self.camera.set(cv2.CAP_PROP_FPS, FPS_VALUE)
        awcr_logger.info(
            f"Camera opened with resolution {CAMERA_WIDTH} x {CAMERA_HEIGHT} and {FPS_VALUE} frames per second."
        )
        return True

    def is_opened(self) -> bool:
        """
        Checks whether the camera is currently opened.

        Returns:
            bool: True if the camera is opened, False otherwise.
        """
        return self.camera is not None and self.camera.isOpened()

    def read_frame(self) -> np.ndarray | None:
        """
        Reads a single frame from the camera and converts it to RGB.

        Returns:
            np.ndarray | None: The frame in RGB format, or None if the camera
            is not opened or the read failed.
        """
        if not self.is_opened():
            return None

        ret, frame = self.camera.read()
        if not ret:
            return None
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def release_camera(self) -> None:
        """
        Releases the camera. Safe to call when the camera was never opened.
        """
        if self.camera is not None:
            self.camera.release()
