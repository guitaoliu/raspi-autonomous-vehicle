import logging
import threading
import time

import numpy as np
import picamera
from picamera.array import PiRGBArray

from utils import convert_jpeg

logger = logging.getLogger(__name__)


class Camera:
    """
    Camera provide entry for get camera frames with formats of BGR numpy ndarray
    and raw jepg.

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
        self.array_np, and the jpeg data is stored in self.frame.
        """
        for r in self._ca.capture_continuous(self.array, "bgr", use_video_port=True):
            self.array_np = np.copy(r.array)
            self.frame = convert_jpeg(self.array_np)
            self.array.truncate(0)
