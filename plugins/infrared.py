import time
import logging

from typing import Tuple
from RPi import GPIO

from config import Config


logger = logging.getLogger(__name__)


class InfraRedSensor:
    """The infrared sensors are mounted on the left and right front of the vehicle and can be used to monitor the presence of obstacles in their corresponding directions.
    """

    def __init__(self) -> None:
        self.left = Config.INFRARED_LEFT_GPIO_BCM
        self.right = Config.INFRARED_RIGHT_GPIO_BCM
        GPIO.setup(self.left, GPIO.IN)
        GPIO.setup(self.right, GPIO.IN)
        logger.debug('Infrared sensor was initialized.')

    def measure(self) -> Tuple[int]:
        """Return the status of infrared sensor, if there is an obstacle, the related result is shown as True. Otherwise the result is False.

        Returns:
            Tuple[bool]: (is_left_activated, is_right_activated)
        """
        left, right = not bool(GPIO.input(self.left)), not bool(
            GPIO.input(self.right)),
        logger.debug(f'Current infrared status: {left}, {right}.')
        return (left, right)


def test_infrared_sensor():
    GPIO.cleanup()
    infrared_sensor = InfraRedSensor()

    try:
        while 1:
            left, right = infrared_sensor.measure()
            time.sleep(0.5)
    except KeyboardInterrupt as e:
        pass
    finally:
        GPIO.cleanup()
