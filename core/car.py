import logging
import threading
import time

from config import CarStatus, Config
from plugins import Camera, InfraRedSensor, Motor, Track, UltrasoundSensor

logger = logging.getLogger(__name__)


class Car:
    def __init__(self, debug: bool) -> None:
        self.status = [
            CarStatus.PAUSE,
        ]
        self.motor = Motor()
        self.camera = Camera()
        self.obstacle = InfraRedSensor()
        self.distance = UltrasoundSensor()
        self.track = Track()

        self.debug = debug

        self.loop = False
        self.operates = {
            CarStatus.INITIALIZE: lambda: self.motor.initialize(),
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

    def __enter__(self):
        self.loop = True
        self._start()
        threading.Thread(target=self._loop).start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.loop = False
        self._stop()

    def track_line(self):
        new_status = self.track(self.camera.array_np)
        self.update(new_status)

    def update(self, new_status: CarStatus) -> None:
        self.status = [
            new_status,
        ]

    def _start(self) -> None:
        self.update(CarStatus.INITIALIZE)
        self.update(CarStatus.PAUSE)

    def _stop(self) -> None:
        self.update(CarStatus.STOP)

    def _loop(self) -> None:
        while self.loop:
            if self.debug:
                time.sleep(1)
            self._move()

    def _move(self) -> None:
        self.operates[self.status[0]]()
