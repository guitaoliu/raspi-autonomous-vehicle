import logging

import cv2
from numpy import ndarray

from config import CarStatus, Config

logger = logging.getLogger(__name__)


class Track:
    def __init__(self):
        self.lines = Config.DETECT_LINE_NUMS

        self._array = None
        self._jpeg = None

    def __call__(self, img: ndarray) -> CarStatus:
        status = self.track(img)
        return status

    @property
    def array(self):
        return self._array

    @property
    def jpeg(self):
        return self._jpeg

    def track(self, img: ndarray) -> CarStatus:
        img = cv2.blur(img, (5, 5))
        _, _, img_red = cv2.split(img)
        _, dst = cv2.threshold(img_red, 20, 255, cv2.THRESH_BINARY)

        height, width = dst.shape
        img_gray = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)
        for i in range(0, height, self.lines):
            pass

        self._array = img_gray
        self.convert_jpeg()

        # todo add control algorithm

        return CarStatus.PAUSE

    def convert_jpeg(self):
        _, buf = cv2.imencode(".jpeg", self._img)
        self._jpeg = buf
