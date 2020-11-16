import logging
import threading
import time

from RPi import GPIO

from config import Config

logger = logging.getLogger(__name__)


class UltrasoundSensor:
    """After instantiating the object, call get_distance
    directly to get the current ultrasonic range result.
    """

    thread = None
    distance = None
    last_access = 0

    trigger = Config.ULTRASOUND_TRIGGER_GPIO_BCM
    echo = Config.ULTRASOUND_ECHO_GPIO_BCM

    def initialize(self) -> None:

        if UltrasoundSensor.thread is None:
            UltrasoundSensor.thread = threading.Thread(
                target=self._thread,
                kwargs={
                    "gpio": GPIO,
                },
            )
            UltrasoundSensor.thread.start()
            while self.distance is None:
                pass

    @classmethod
    def _thread(cls, gpio: GPIO) -> None:
        """A seperated thread for ultrasound distance measurement."""
        while True:
            time.sleep(Config.ULTRASOUND_SAMPLING_INTERVAL)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(cls.trigger, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(cls.echo, GPIO.IN)
            GPIO.output(cls.trigger, 1)
            time.sleep(0.00001)
            GPIO.output(cls.trigger, 0)

            ch = GPIO.wait_for_edge(cls.echo, GPIO.RISING, timeout=100)
            if ch:
                start = time.time()
                while gpio.input(cls.echo) == 1:
                    pass
                time_elapsed = time.time() - start
                cls.distance = 34000 * time_elapsed / 2
                logger.debug(f"Distance measured as {cls.distance}cm")
            else:
                logger.debug("Lost echo wave")
                cls.distance = -1

            if time.time() - cls.last_access > 5000:
                break

        cls.thread = None
        cls.distance = None

    def get_distance(self) -> float:
        """get the measure result of ultrasound sensor. The result is in centermeter.

        Returns:
            float: measure result.
        """
        UltrasoundSensor.last_access = time.time()
        self.initialize()
        return self.distance


def test_ultrasoud():
    ultrasound_sensor = UltrasoundSensor()
    try:
        distance = ultrasound_sensor.get_distance()
    except KeyboardInterrupt as e:
        pass
    finally:
        GPIO.cleanup()