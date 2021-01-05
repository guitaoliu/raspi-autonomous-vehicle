import logging
import time

from RPi import GPIO

from config import Config

logger = logging.getLogger(__name__)


class UltrasoundSensor:
    """
    Ultrasonic sensors are installed in front of the car and can be used to obtain the
    distance between the obstacle and the car.
    """

    def __init__(self) -> None:
        self.trigger = Config.ULTRASOUND_TRIGGER_GPIO_BCM
        self.echo = Config.ULTRASOUND_ECHO_GPIO_BCM
        GPIO.setup(self.trigger, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.echo, GPIO.IN)

        self._last = 0
        self._current = 0

    def __call__(self) -> float:
        """
        Call the object to get the measure result of ultrasound sensor.
        The result is in centimeter.

        Returns:
            float: measure result.
        """
        GPIO.output(self.trigger, 1)
        time.sleep(0.00001)
        GPIO.output(self.trigger, 0)
        ch = GPIO.wait_for_edge(self.echo, GPIO.RISING, timeout=300)
        if ch:
            start = time.perf_counter()
            while GPIO.input(self.echo) == 1:
                pass
            time_elapsed = time.perf_counter() - start
            distance = 34000 * time_elapsed / 2
            logger.debug(f"Current front distance: {distance}.")
        else:
            distance = 999999
            logger.warning("Cannot get front distance.")
            return distance

        self._last = self._moving_average(distance, self._last, 0.8)
        return self._last

    @staticmethod
    def _moving_average(a: float, b: float, per: float) -> float:
        return per * a + (1 - per) * b
