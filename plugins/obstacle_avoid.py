import logging
from typing import Tuple

from config import CarStatus

logger = logging.getLogger(__name__)


class ObstacleAvoid:
    """
    The obstacle avoidance module makes decisions based on the status of the ultrasound
    and infrared sensors and returns the next CarStatus.
    """

    def __init__(self):
        pass

    def __call__(
        self, distance: float, obstacle_status: Tuple[bool, bool]
    ) -> CarStatus:
        """

        Args:
            distance: the result of ultrasound sensor
            obstacle_status: the result of infrared sensor

        Returns:
            CarStatus: next CarStatus
        """
        left, right = obstacle_status
        logger.debug(f"Car status: left: {left}, right: {right}, distance: {distance}")
        if left and not right:
            return CarStatus.RIGHT
        elif not left and right:
            return CarStatus.LEFT
        elif left and right:
            return CarStatus.BACKWARD
        else:
            if distance < 40:
                return CarStatus.LEFT
            elif distance < 100:
                return CarStatus.FORWARD_SLOW
            else:
                return CarStatus.FORWARD
