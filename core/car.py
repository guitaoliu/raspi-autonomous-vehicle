import logging
import threading
import time

from config import CarStatus, Config
from plugins import (
    Camera,
    Controller,
    InfraRedSensor,
    Motor,
    ObstacleAvoid,
    Track,
    UltrasoundSensor,
)

logger = logging.getLogger(__name__)


class Car:
    def __init__(self) -> None:
        self._status = [
            CarStatus.PAUSE,
        ]

        # Plugins initialized
        self.motor = Motor()
        self.camera = Camera()
        self.obstacle = InfraRedSensor()
        self.distance = UltrasoundSensor()
        self.track = Track()
        self.obstacle_avoid = ObstacleAvoid()
        self.controller = Controller()

        # Motor related configs
        self._is_loop = False
        self._operates = {
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
        self._is_loop = True
        self._start()
        threading.Thread(target=self._loop).start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._is_loop = False
        self._stop()

    @property
    def status(self) -> CarStatus:
        return self._status[0]

    def run(self, method: str):
        if method == "two_line_track":
            self.track.get_perspective_transform(self.camera.array_np)
            while True:
                time.sleep(Config.TRACK_PROCESS_INTERVAL)
                self._track_line()
        elif method == "obstacle_avoid":
            while True:
                time.sleep(Config.TRACK_PROCESS_INTERVAL)
                self._obstacle_avoid()
        elif method == "bluetooth_controller":
            while True:
                time.sleep(Config.TRACK_PROCESS_INTERVAL)
                self._bluetooth_controller()
        elif method == "debug":
            while True:
                time.sleep(Config.TRACK_PROCESS_INTERVAL)
        else:
            logger.fatal(f"Method {' '.join(method.split('_'))} is not supported")

    def _obstacle_avoid(self):
        status = self.obstacle_avoid(
            obstacle_status=self.obstacle(), distance=self.distance()
        )
        self._update(status)

    def _track_line(self):
        status = self.track(self.camera.array_np)
        self._update(status)

    def _bluetooth_controller(self):
        status = self.controller()
        self._update(status)

    def _update(self, new_status: CarStatus) -> None:
        self._status = [
            new_status,
        ]

    def _start(self) -> None:
        self.motor.initialize()
        self._update(CarStatus.PAUSE)

    def _stop(self) -> None:
        self.motor.stop()
        self._update(CarStatus.STOP)

    def _loop(self) -> None:
        while self._is_loop:
            self._move()

    def _move(self) -> None:
        self._operates[self._status[0]]()
