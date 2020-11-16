import enum

from plugins import Camera, InfraRedSensor, Motor, UltrasoundSensor


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
    BACKWORD = enum.auto()
    FAST_BACKWORD = enum.auto()
    SLOW_BACKWORD = enum.auto()


class Car:
    status = CarStatus

    def __init__(self) -> None:
        self.status = CarStatus.STOP
        self.motor = Motor()
        self.motor.initital()
        infra_red_sensor = InfraRedSensor()
        self.get_obstacle = infra_red_sensor.get_result
        ultrasound_sensor = UltrasoundSensor()
        self.get_distance = ultrasound_sensor.get_distance
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
        elif self.status == CarStatus.BACKWORD:
            self.motor.backword(50)
            return True
        elif self.status == CarStatus.FAST_BACKWORD:
            self.motor.backword(80)
            return True
        elif self.status == CarStatus.SLOW_BACKWORD:
            self.motor.backword(30)
            return True
        else:
            return False
