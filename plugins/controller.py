import evdev

from config import CarStatus


class Controller:
    def __init__(self):
        self.device = evdev.InputDevice("/dev/input/event0")
        self.A = evdev.ecodes.BTN_A
        self.B = evdev.ecodes.BTN_B
        self.X = evdev.ecodes.BTN_X
        self.Y = evdev.ecodes.BTN_Y
        self.LB = evdev.ecodes.BTN_TL
        self.RB = evdev.ecodes.BTN_TR

        self.axis_x = evdev.ecodes.ABS_X
        self.axis_y = evdev.ecodes.ABS_Y

    def __call__(self) -> CarStatus:
        x = self.device.absinfo(self.axis_x)
        y = self.device.absinfo(self.axis_y)
        if abs(y.value) > y.flat * 2:
            if y.value > 0:
                return CarStatus.RIGHT
            else:
                return CarStatus.LEFT
        elif abs(x.value) > x.flat:
            if x.value > 0:
                return CarStatus.FORWARD
            else:
                return CarStatus.BACKWARD
        else:
            return CarStatus.PAUSE
