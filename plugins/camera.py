import logging
import threading
import time

import cv2
import numpy as np
import picamera
from picamera.array import PiRGBArray

logger = logging.getLogger(__name__)


class Camera:
    """Camera provide entry for get camera frames with formats of BGR numpy ndarray
    and raw jepg.

    Please use Camera with context manager to avoid not closing the camera rightly.

    """

    def __init__(self) -> None:
        self._ca = picamera.PiCamera()
        self._ca.resolution = (640, 480)
        self._ca.framerate = 32

        self.array = PiRGBArray(self._ca, size=(640, 480))
        self.array_np = None
        self.frame = None
        self.start()

    def start(self) -> None:
        self._ca.start_preview()
        time.sleep(1)
        logger.debug("Camera started")
        threading.Thread(target=lambda: self._gen()).start()
        time.sleep(1)

    def close(self):
        logger.debug("Camera stopped")
        self._ca.close()

    def _gen(self):
        """
        Generate raw numpy array and jpeg raw data. The numpy array is stored in
        self.array_np, and the jpeg data isstored in self.frame.
        """
        for r in self._ca.capture_continuous(self.array, "bgr", use_video_port=True):
            self.array_np = np.copy(r.array)
            self._jpeg()
            self.array.truncate(0)

    def _jpeg(self):
        """
        Convert raw numpy array to jpeg data.
        """
        _, buf = cv2.imencode(".jpeg", self.array_np)
        self.frame = buf
