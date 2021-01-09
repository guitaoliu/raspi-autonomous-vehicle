import enum


class Config:
    MOTOR_1_GPIO_BCM = 5
    MOTOR_2_GPIO_BCM = 6
    MOTOR_3_GPIO_BCM = 19
    MOTOR_4_GPIO_BCM = 26

    INFRARED_LEFT_GPIO_BCM = 21
    INFRARED_RIGHT_GPIO_BCM = 20

    ULTRASOUND_ECHO_GPIO_BCM = 12
    ULTRASOUND_TRIGGER_GPIO_BCM = 16

    SPEED_NORMAL = 50
    SPEED_FAST = 80
    SPEED_SLOW = 30

    TRACK_PROCESS_INTERVAL = 0.1
    PROCESS_LINES = 10
    DETECT_OFFSET = 50


class CarStatus(enum.Enum):
    NONE = enum.auto
    STOP = enum.auto()
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


class PathType(enum.Enum):
    BothSides = enum.auto()
    OneSide = enum.auto()
    NonSide = enum.auto()
