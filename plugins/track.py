import logging

import cv2
from numpy import ndarray

from config import CarStatus, Config
from plugins.image_processing import processing, strategy, perspective_transform

logger = logging.getLogger(__name__)


class Track:
    def __init__(self):
        self.lines = Config.DETECT_LINE_NUMS

        self._array = None
        self._jpeg = None
        self._transform_matrix = None

    def __call__(self, img: ndarray) -> CarStatus:
        status = self.tr(img)
        return status

    @property
    def array(self):
        return self._array

    @property
    def jpeg(self):
        return self._jpeg

    @property
    def transform_matrix(self):
        return self._transform_matrix

    def tr(self, img: ndarray) -> CarStatus:
        img_red, dst, img_gray = processing(img, self._transform_matrix, self.lines)

        self._array = img_gray
        self.convert_jpeg()

        car_status = strategy(img_gray)

        return car_status

    def convert_jpeg(self):
        _, buf = cv2.imencode(".jpeg", self.array)
        self._jpeg = buf

    def get_perspective_transform(self, img: ndarray):
        self._transform_matrix = perspective_transform(img)
