import enum
import logging
import threading

from config import Config
from sensors import InfraRedSensor, Motor, UltrasoundSensor

logger = logging.getLogger(__name__)


class CarStatus(enum.Enum):
    STOP = 0
    PAUSE = enum.auto()
    FORWARD = enum.auto()
    FORWARD_FAST = enum.auto()
    FORWARD_SLOW = enum.auto()
    LEFT = enum.auto()
    LEFT_FAST = enum.auto()
    LEFT_SLOW = enum.auto()
    RIGHT = enum.auto()
    RIGHT_FAST = enum.auto()
    RIGHT_SLOW = enum.auto()
    BACKWARD = enum.auto()
    BACKWARD_FAST = enum.auto()
    BACKWARD_SLOW = enum.auto()


class Car:
    status = CarStatus

    def __init__(self) -> None:
        self.status = CarStatus.PAUSE
        self.motor = Motor()
        self.obstacle = InfraRedSensor()
        self.distance = UltrasoundSensor()

        self.loop = False
        self.operates = {
            CarStatus.STOP: lambda: self.motor.stop(),
            CarStatus.PAUSE: lambda: self.motor.pause(),
            CarStatus.FORWARD: lambda: self.motor.forward(Config.SPEED_NORMAL),
            CarStatus.FORWARD_FAST: lambda: self.motor.forward(Config.SPEED_FAST),
            CarStatus.FORWARD_SLOW: lambda: self.motor.forward(Config.SPEED_SLOW),
            CarStatus.LEFT: lambda: self.motor.turn_left_in_place(Config.SPEED_NORMAL),
            CarStatus.LEFT_FAST: lambda: self.motor.turn_left_in_place(
                Config.SPEED_FAST
            ),
            CarStatus.LEFT_SLOW: lambda: self.motor.turn_left_in_place(
                Config.SPEED_SLOW
            ),
            CarStatus.RIGHT: lambda: self.motor.turn_right_in_place(
                Config.SPEED_NORMAL
            ),
            CarStatus.RIGHT_FAST: lambda: self.motor.turn_right_in_place(
                Config.SPEED_FAST
            ),
            CarStatus.RIGHT_SLOW: lambda: self.motor.turn_right_in_place(
                Config.SPEED_SLOW
            ),
            CarStatus.BACKWARD: lambda: self.motor.backward(Config.SPEED_NORMAL),
            CarStatus.BACKWARD_FAST: lambda: self.motor.backward(Config.SPEED_FAST),
            CarStatus.BACKWARD_SLOW: lambda: self.motor.backward(Config.SPEED_SLOW),
        }

    def update(self, new_status: CarStatus) -> None:
        self.status = new_status

    def __enter__(self):
        self.loop = True
        self._start()
        threading.Thread(target=self._loop).start()
        logger.debug("Car motor started.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.loop = False
        self._stop()
        logger.debug("Car motor stopped.")

    def _start(self) -> None:
        self.motor.initialize()
        self.update(CarStatus.PAUSE)

    def _stop(self) -> None:
        self.update(CarStatus.STOP)

    def _loop(self) -> None:
        while self.loop:
            logger.debug(f"Current status: {self.status}")
            self._move()

    def _move(self) -> None:
        self.operates[self.status]()
