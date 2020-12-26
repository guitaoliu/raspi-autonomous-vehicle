import logging
from typing import Tuple

from config import CarStatus

logger = logging.getLogger(__name__)


class ObstacleAvoid:
    def __init__(self):
        pass

    def __call__(
        self, distance: float, obstacle_status: Tuple[bool, bool]
    ) -> CarStatus:
        left, right = obstacle_status
        logger.info(f"Car status: left: {left}, right: {right}, distance: {distance}")
        if left and not right:
            return CarStatus.RIGHT
        elif not left and right:
            return CarStatus.LEFT
        elif left and right:
            return CarStatus.BACKWARD
        else:
            if distance < 20:
                return CarStatus.LEFT
            elif distance < 100:
                return CarStatus.FORWARD
            else:
                return CarStatus.FORWARD_FAST
