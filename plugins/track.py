import logging

import cv2
from numpy import ndarray
from plugins.image_processing import processing, strategy

from config import CarStatus, Config

logger = logging.getLogger(__name__)


class Track:
    def __init__(self):
        self.lines = Config.DETECT_LINE_NUMS

        self._array = None
        self._jpeg = None

    def __call__(self, img: ndarray) -> CarStatus:
        status = self.tr(img)
        return status

    @property
    def array(self):
        return self._array

    @property
    def jpeg(self):
        return self._jpeg

    def tr(self, img: ndarray) -> CarStatus:
        img_red, dst, img_gray = processing(img, self.lines)

        self._array = img_gray
        self.convert_jpeg()

        car_status = strategy(img_gray)

        return car_status

    def convert_jpeg(self):
        _, buf = cv2.imencode(".jpeg", self.array)
        self._jpeg = buf
