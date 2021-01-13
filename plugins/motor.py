import logging

import RPi.GPIO as GPIO

from config import Config

logger = logging.getLogger(__name__)


class Motor:
    """Motor is for controlling the movement of the car."""

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Config.MOTOR_1_GPIO_BCM, GPIO.OUT)
        GPIO.setup(Config.MOTOR_2_GPIO_BCM, GPIO.OUT)
        GPIO.setup(Config.MOTOR_3_GPIO_BCM, GPIO.OUT)
        GPIO.setup(Config.MOTOR_4_GPIO_BCM, GPIO.OUT)

        self.motor_1 = GPIO.PWM(Config.MOTOR_1_GPIO_BCM, 500)
        self.motor_2 = GPIO.PWM(Config.MOTOR_2_GPIO_BCM, 500)
        self.motor_3 = GPIO.PWM(Config.MOTOR_3_GPIO_BCM, 500)
        self.motor_4 = GPIO.PWM(Config.MOTOR_4_GPIO_BCM, 500)

    def initialize(self) -> None:
        """Initialized the motor"""
        self.motor_1.start(0)
        self.motor_2.start(0)
        self.motor_3.start(0)
        self.motor_4.start(0)
        # logger.debug("Motor was initialized.")

    def stop(self) -> None:
        """Stop the motor engine.
        After this process, you need to call Motor.initialize to initialize the motor.
        """
        self.motor_1.stop()
        self.motor_2.stop()
        self.motor_3.stop()
        self.motor_4.stop()
        # logger.debug("Motor done.")

    def forward(self, speed: int) -> None:
        """Move forward

        Args:
            speed (int): motor electrical signal duty cycle, from 0 to 100.
        """
        self.motor_1.ChangeDutyCycle(speed)
        self.motor_2.ChangeDutyCycle(0)
        self.motor_3.ChangeDutyCycle(speed)
        self.motor_4.ChangeDutyCycle(0)
        # logger.debug("Move forward!")

    def backward(self, speed: int) -> None:
        """Move backward

        Args:
            speed (int): motor electrical signal duty cycle, from 0 to 100.
        """
        self.motor_1.ChangeDutyCycle(0)
        self.motor_2.ChangeDutyCycle(speed)
        self.motor_3.ChangeDutyCycle(0)
        self.motor_4.ChangeDutyCycle(speed)
        # logger.debug("Move backward!")

    def pause(self) -> None:
        """Stop the car"""
        self.motor_1.ChangeDutyCycle(0)
        self.motor_2.ChangeDutyCycle(0)
        self.motor_3.ChangeDutyCycle(0)
        self.motor_4.ChangeDutyCycle(0)
        # logger.debug("Pause")

    def turn_right_in_place(self, speed: int) -> None:
        """Turn left with the left back wheel as the origin.

        Args:
            speed (int): motor electrical signal duty cycle。
        """
        self.motor_1.ChangeDutyCycle(0)
        self.motor_2.ChangeDutyCycle(0)
        self.motor_3.ChangeDutyCycle(speed)
        self.motor_4.ChangeDutyCycle(0)
        # logger.debug("Turn right.")

    def turn_left_in_place(self, speed: int) -> None:
        """Turn right with the right back wheel as the origin.

        Args:
            speed (int): motor electrical signal duty cycle。
        """
        self.motor_1.ChangeDutyCycle(speed)
        self.motor_2.ChangeDutyCycle(0)
        self.motor_3.ChangeDutyCycle(0)
        self.motor_4.ChangeDutyCycle(0)
        # logger.debug("Turn left.")
