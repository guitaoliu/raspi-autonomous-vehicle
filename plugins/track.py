import logging
import time
from typing import Optional

import cv2
import numpy as np
from numpy import ndarray

from config import CarStatus, Config

logger = logging.getLogger(__name__)


class Track:
    def __init__(self) -> None:
        self._jpeg = None
        self._lines = Config.PROCESS_LINES

    def __call__(self, img: ndarray, method: Optional[str] = "basic") -> CarStatus:
        if method == "basic":
            status = self.basic(img)
        else:
            status = CarStatus.PAUSE
            logger.fatal(f"unknown method {method}")
        return status

    @property
    def jpeg(self) -> ndarray:
        return self._jpeg

    def basic(self, img: ndarray) -> CarStatus:
        start = time.perf_counter()
        img = cv2.blur(img, (5, 5))
        _, _, img_red = cv2.split(img)
        _, dst = cv2.threshold(img_red, 20, 255, cv2.THRESH_BINARY)

        height, width = dst.shape
        points_left = np.zeros(self._lines)
        points_right = np.zeros(self._lines)
        img_gray = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)
        self._jpeg = img_gray

        for i in range(self._lines):
            current_height = height - 1 - 15 * (i + 1)
            img_left = img_gray[current_height, 0 : width // 2]
            img_right = img_gray[current_height, width // 2 : width]
            line_left, line_right = np.where(img_left == 0), np.where(img_right == 0)

            if len(line_left[0]):
                points_left[i] = np.mean(line_left[0])
            else:
                points_left[i] = 0

            if len(line_right[0]):
                points_right[i] = np.mean(line_right[0]) + width // 2
            else:
                points_right[i] = width - 1

        left_valid = [p for p in points_left if p != 0]
        right_valid = [p for p in points_right if p != width - 1]

        left = np.max(left_valid) if left_valid else None
        right = np.min(right_valid) if right_valid else None

        logger.debug(f"{time.perf_counter() - start:.2}s time elapsed")

        if not left and not right:
            return CarStatus.NONE
        elif left and not right:
            if left < Config.SET_FORWARD:
                return CarStatus.FORWARD_SLOW
            elif left < Config.SET_SLOW_TURN:
                return CarStatus.RIGHT_SLOW
            elif left < Config.SET_FAST_TURN:
                return CarStatus.RIGHT
            else:
                return CarStatus.LEFT
        elif not left and right:
            offset = width - right
            if offset < Config.SET_FORWARD:
                return CarStatus.FORWARD_SLOW
            elif offset < Config.SET_SLOW_TURN:
                return CarStatus.LEFT_SLOW
            elif offset < Config.SET_FAST_TURN:
                return CarStatus.LEFT
            else:
                return CarStatus.RIGHT
        else:
            return CarStatus.FORWARD_SLOW
