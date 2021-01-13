import logging
from typing import Optional

import cv2
import numpy as np
from numpy import ndarray

from config import CarStatus, Config
from utils import convert_jpeg

logger = logging.getLogger(__name__)


class Track:
    def __init__(self):
        self._jpeg = None
        self._lines = Config.PROCESS_LINES

    def __call__(self, img: ndarray, method: Optional[str] = "basic") -> CarStatus:
        if method == "basic":
            status = self.basic(img)
        elif method == "two":
            status = self.other(img)
        else:
            status = CarStatus.PAUSE
            logger.fatal(f"unknown method {method}")
        return status

    @property
    def jpeg(self):
        return self._jpeg

    def other(self, img: ndarray) -> CarStatus:
        dst = img
        self._jpeg = convert_jpeg(dst)
        return CarStatus.PAUSE

    def basic(self, img: ndarray) -> CarStatus:
        img = cv2.blur(img, (5, 5))
        img_green, img_blue, img_red = cv2.split(img)
        _, dst = cv2.threshold(img_red, 20, 255, cv2.THRESH_BINARY)

        height, width = dst.shape
        points_left = np.zeros(self._lines)
        points_right = np.zeros(self._lines)
        img_gray = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)

        for i in range(self._lines):
            current_height = height - 1 - 15 * (i + 1)
            img_left = img_gray[current_height, 0 : width // 2]
            img_right = img_gray[current_height, width // 2 : width]
            line_left, line_right = np.where(img_left == 0), np.where(img_right == 0)

            if len(line_left[0]):
                points_left[i] = np.mean(line_left[0])
                img_gray = cv2.circle(
                    img_gray, (int(points_left[i]), current_height), 4, (0, 0, 255), 5
                )
            else:
                points_left[i] = 0

            if len(line_right[0]):
                points_right[i] = np.mean(line_right[0]) + width // 2
                img_gray = cv2.circle(
                    img_gray, (int(points_right[i]), current_height), 4, (0, 0, 255), 5
                )
            else:
                points_right[i] = width - 1

        self._jpeg = convert_jpeg(img_gray)

        left_valid = [p for p in points_left if p != 0]
        right_valid = [p for p in points_right if p != width - 1]

        left = np.max(left_valid) if left_valid else None
        right = np.min(right_valid) if right_valid else None

        if left and right:
            logger.debug("Detected both lines")
            return CarStatus.FORWARD_SLOW
        elif left and not right:
            logger.debug("No right line detected")
            if left < Config.DETECT_OFFSET:
                return CarStatus.FORWARD_SLOW
            elif left < width / 2 - Config.CENTRAL_OFFSET:
                return CarStatus.RIGHT_SLOW
            else:
                return CarStatus.RIGHT
        elif not left and right:
            logger.debug("No left line detected")
            if right > width - Config.DETECT_OFFSET:
                return CarStatus.FORWARD_SLOW
            elif right > width / 2 + Config.CENTRAL_OFFSET:
                return CarStatus.LEFT_SLOW
            else:
                return CarStatus.LEFT
        else:
            return CarStatus.NONE
