import logging
from typing import Tuple

from RPi import GPIO

from config import Config

logger = logging.getLogger(__name__)


class InfraRedSensor:
    """
    The infrared sensors are mounted on the left and right front of the vehicle
    and can be used to monitor the presence of obstacles in their corresponding
    direction.
    """

    def __init__(self):
        self.left = Config.INFRARED_LEFT_GPIO_BCM
        self.right = Config.INFRARED_RIGHT_GPIO_BCM
        GPIO.setup(self.left, GPIO.IN)
        GPIO.setup(self.right, GPIO.IN)

    def __call__(self) -> Tuple[bool, bool]:
        """
        Return the status of infrared sensor, if there is an obstacle, the related
        result is shown as True. Otherwise the result is False.

        Returns:
            Tuple[bool]: (is_left_activated, is_right_activated)
        """
        left = not bool(GPIO.input(self.left))
        right = not bool(GPIO.input(self.right))
        logger.debug(f"Infrared Status: {left}, {right}")
        return left, right
