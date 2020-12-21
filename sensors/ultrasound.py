import logging
import time
from typing import Optional

from RPi import GPIO

from config import Config

logger = logging.getLogger(__name__)


class UltrasoundSensor:
    """After instantiating the object, call the object
    directly to get the current ultrasonic range result.
    """

    def __init__(self) -> None:
        self.trigger = Config.ULTRASOUND_TRIGGER_GPIO_BCM
        self.echo = Config.ULTRASOUND_ECHO_GPIO_BCM
        GPIO.setup(self.trigger, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.echo, GPIO.IN)

    def __call__(self) -> float:
        return self.value()

    def value(self) -> Optional[float]:
        """get the measure result of ultrasound sensor. The result is in centermeter.

        Returns:
            float: measure result.
        """
        GPIO.output(self.trigger, 1)
        time.sleep(0.00001)
        GPIO.output(self.trigger, 0)
        ch = GPIO.wait_for_edge(self.echo, GPIO.RISING, timeout=100)
        if ch:
            start = time.perf_counter()
            while GPIO.input(self.echo) == 1:
                pass
            time_elapsed = time.perf_counter() - start
            distance = 34000 * time_elapsed / 2
            logger.debug(f"Current front distance: {distance}.")
        else:
            distance = None
            logger.warning("Cannot get front distance.")
        return distance


def test_ultrasound():
    GPIO.setmode(GPIO.BCM)
    sensor = UltrasoundSensor()
    try:
        while True:
            time.sleep(0.5)
            d = sensor()
            print(d)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    test_ultrasound()
