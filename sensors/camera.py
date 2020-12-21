import logging
import threading
import time

import cv2
import numpy as np
import picamera
from picamera.array import PiRGBArray

logger = logging.getLogger(__name__)


class Camera:
    """Camera provide entry for get camera frames with formats of BGR numpy ndarray and raw jepg.

    Please use Camera with context manager to avoid not closing the camera rightly.

    """

    def __init__(self) -> None:
        self.ca = picamera.PiCamera()
        self.ca.resolution = (640, 480)
        self.ca.framerate = 32

        self.array = PiRGBArray(self.ca, size=(640, 480))
        self.array_np = None
        self.frame = None

    def __enter__(self):
        logger.debug("Camera started.")
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Camera closed.")
        self.ca.close()

    def start(self) -> None:
        self.ca.start_preview()

        time.sleep(1)
        print("Process started")
        threading.Thread(target=lambda: self._gen()).start()
        time.sleep(1)

    def close(self):
        self.ca.close()

    def _gen(self):
        """
        Generate raw numpy array and jpeg raw data. The numpy array is stored in self.array_np, and the jpeg data is
        stored in self.frame.
        """
        for r in self.ca.capture_continuous(self.array, "bgr", use_video_port=True):
            self.array_np = np.copy(r.array)
            self._jpeg()
            self.array.truncate(0)

    def _jpeg(self):
        """
        Convert raw numpy array to jpeg data.
        """
        _, buf = cv2.imencode(".jpeg", self.array_np)
        self.frame = buf
