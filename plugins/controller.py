import logging
from typing import Optional, Tuple

import evdev

from config import CarStatus

logger = logging.getLogger(__name__)


class Controller:
    """
    The controller provides interaction with the xbox one gamepad to control movement
    via the left stick, and RB and LB button provide deceleration and acceleration
    functions respectively.
    """

    def __init__(self, device: Optional[str] = "/dev/input/event0"):
        try:
            self.device = evdev.InputDevice(device)
        except FileNotFoundError:
            self.device = None
            logger.debug(f"Gamepad {device} is not connected")

        self.A = evdev.ecodes.BTN_A
        self.B = evdev.ecodes.BTN_B
        self.X = evdev.ecodes.BTN_X
        self.Y = evdev.ecodes.BTN_Y
        self.LB = evdev.ecodes.BTN_TL
        self.RB = evdev.ecodes.BTN_TR

        self.axis_x = evdev.ecodes.ABS_X
        self.axis_y = evdev.ecodes.ABS_Y

    def __call__(self) -> CarStatus:
        """
        Call the object to get next CarStatus based on Controller's status.
        Returns:
            CarStatus: Car movement status
        """
        if self.device is not None:
            x = self.device.absinfo(self.axis_x)
            y = self.device.absinfo(self.axis_y)
            keys = self.device.active_keys()
            if abs(x.value) > x.flat * 6:
                if x.value > 0:
                    return self._right(keys)
                else:
                    return self._left(keys)
            elif abs(y.value) > y.flat:
                if y.value < 0:
                    return self._forward(keys)
                else:
                    return self._backward(keys)
            else:
                return CarStatus.PAUSE
        else:
            logger.fatal("Gamepad initialized failed, please connect it first.")

    def _left(self, keys: Tuple[int]) -> CarStatus:
        if self.LB in keys:
            return CarStatus.LEFT_FAST
        elif self.RB in keys:
            return CarStatus.LEFT_SLOW
        else:
            return CarStatus.LEFT

    def _right(self, keys: Tuple[int]) -> CarStatus:
        if self.LB in keys:
            return CarStatus.RIGHT_FAST
        elif self.RB in keys:
            return CarStatus.RIGHT_SLOW
        else:
            return CarStatus.RIGHT

    def _forward(self, keys: Tuple[int]) -> CarStatus:
        if self.LB in keys:
            return CarStatus.FORWARD_FAST
        elif self.RB in keys:
            return CarStatus.FORWARD_SLOW
        else:
            return CarStatus.FORWARD

    def _backward(self, keys: Tuple[int]) -> CarStatus:
        if self.LB in keys:
            return CarStatus.BACKWARD_FAST
        elif self.RB in keys:
            return CarStatus.BACKWARD_SLOW
        else:
            return CarStatus.BACKWARD
