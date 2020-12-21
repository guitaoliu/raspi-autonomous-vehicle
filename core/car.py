import enum

from sensors import *


class CarStatus(enum.Enum):
    STOP = 0
    FORWARD = enum.auto()
    FAST_FORWARD = enum.auto()
    SLOW_FORWARD = enum.auto()
    LEFT = enum.auto()
    FAST_LEFT = enum.auto()
    SLOW_LEFT = enum.auto()
    RIGHT = enum.auto()
    FAST_RIGHT = enum.auto()
    SLOW_RIGHT = enum.auto()
    BACKWARD = enum.auto()
    FAST_BACKWARD = enum.auto()
    SLOW_BACKWARD = enum.auto()


class Car:
    status = CarStatus

    def __init__(self) -> None:
        self.status = CarStatus.STOP
        self.motor = Motor()
        self.motor.initialize()
        self.get_obstacle = InfraRedSensor()
        self.get_distance = UltrasoundSensor()
        self.update_move_status(CarStatus.FORWARD)

    def update_move_status(self, new_status: CarStatus) -> None:
        self.status = new_status

    def loop(self) -> None:
        while True:
            self.move()

    def move(self) -> bool:
        if self.status == CarStatus.STOP:
            self.motor.pause()
            return True
        elif self.status == CarStatus.FORWARD:
            self.motor.forward(50)
            return True
        elif self.status == CarStatus.FAST_FORWARD:
            self.motor.forward(80)
            return True
        elif self.status == CarStatus.SLOW_FORWARD:
            self.motor.forward(30)
            return True
        elif self.status == CarStatus.LEFT:
            self.motor.turn_left_in_place(50)
            return True
        elif self.status == CarStatus.FAST_LEFT:
            self.motor.turn_left_in_place(80)
            return True
        elif self.status == CarStatus.SLOW_LEFT:
            self.motor.turn_left_in_place(30)
            return True
        elif self.status == CarStatus.RIGHT:
            self.motor.turn_right_in_place(50)
            return True
        elif self.status == CarStatus.FAST_RIGHT:
            self.motor.turn_right_in_place(80)
            return True
        elif self.status == CarStatus.SLOW_RIGHT:
            self.motor.turn_right_in_place(30)
            return True
        elif self.status == CarStatus.BACKWARD:
            self.motor.backward(50)
            return True
        elif self.status == CarStatus.FAST_BACKWARD:
            self.motor.backward(80)
            return True
        elif self.status == CarStatus.SLOW_BACKWARD:
            self.motor.backward(30)
            return True
        else:
            return False
