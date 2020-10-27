import time
import logging
import threading

from typing import Tuple
from RPi import GPIO

from config import Config


logger = logging.getLogger(__name__)


class InfraRedSensor:
    """The infrared sensors are mounted on the left and right front of the vehicle and can be used to monitor the presence of obstacles in their corresponding directions.
    """
    thread = None
    last_access = 0
    left, right = False, False
    left_GPIO = Config.INFRARED_LEFT_GPIO_BCM
    right_GPIO = Config.INFRARED_RIGHT_GPIO_BCM

    def initialize(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left_GPIO, GPIO.IN)
        GPIO.setup(self.right, GPIO.IN)

        if InfraRedSensor.thread is None:
            InfraRedSensor.last_access = time.time()
            InfraRedSensor.thread = threading.Thread(target=self._thread)
            InfraRedSensor.thread.start()
            logger.debug('Infrared sensor was initialized.')

    def get_result(self) -> Tuple[bool]:
        """Return the status of infrared sensor, if there is an obstacle, the related result is shown as True. Otherwise the result is False.

        Returns:
            Tuple[bool]: (is_left_activated, is_right_activated)
        """
        InfraRedSensor.last_access = time.time()
        self.initialize()
        return self.left, self.right

    @classmethod
    def _thread(cls):

        while True:
            time.sleep(Config.INFRARED_SAMPLING_INTERVAL)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(cls.left_GPIO, GPIO.IN)
            GPIO.setup(cls.right_GPIO, GPIO.IN)
            cls.left = not bool(GPIO.input(cls.left_GPIO))
            cls.right = not bool(GPIO.input(cls.right_GPIO))
            logger.debug(f'Current infrared status: {cls.left}, {cls.right}.')

            if time.time() - cls.last_access > 5000:
                break
        cls.thread = None


def test_infrared_sensor():
    GPIO.cleanup()
    infrared_sensor = InfraRedSensor()
    try:
        left, right = infrared_sensor.get_result()
    except KeyboardInterrupt as e:
        pass
    finally:
        GPIO.cleanup()
