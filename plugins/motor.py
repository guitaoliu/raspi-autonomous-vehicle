import time

import RPi.GPIO as GPIO

from config import Config


class Motor:

    def __init__(self):
        """Motor is for controlling the movement of the car.
        """
        GPIO.setup(Config.MOTOR_1_GPIO_BCM, GPIO.OUT)
        GPIO.setup(Config.MOTOR_2_GPIO_BCM, GPIO.OUT)
        GPIO.setup(Config.MOTOR_3_GPIO_BCM, GPIO.OUT)
        GPIO.setup(Config.MOTOR_4_GPIO_BCM, GPIO.OUT)

        self.motor_1 = GPIO.PWM(Config.MOTOR_1_GPIO_BCM, 500)
        self.motor_2 = GPIO.PWM(Config.MOTOR_2_GPIO_BCM, 500)
        self.motor_3 = GPIO.PWM(Config.MOTOR_3_GPIO_BCM, 500)
        self.motor_4 = GPIO.PWM(Config.MOTOR_4_GPIO_BCM, 500)

        self.initital()

    def initital(self) -> None:
        """Initialized the motor
        """
        self.motor_1.start(0)
        self.motor_2.start(0)
        self.motor_3.start(0)
        self.motor_4.start(0)

    def stop(self) -> None:
        """Stop the motor engine. After this process, you need to call Motor.initital to initialize the motor.
        """
        self.motor_1.stop()
        self.motor_2.stop()
        self.motor_3.stop()
        self.motor_4.stop()

    def forward(self, speed: int) -> None:
        """Move forward

        Args:
            speed (int): motor electrical signal duty cycle, from 0 to 100.
        """
        self.motor_1.ChangeDutyCycle(speed)
        self.motor_2.ChangeDutyCycle(0)
        self.motor_3.ChangeDutyCycle(speed)
        self.motor_4.ChangeDutyCycle(0)

    def backword(self, speed: int) -> None:
        """Move backword

        Args:
            speed (int): motor electrical signal duty cycle, from 0 to 100.
        """
        self.motor_1.ChangeDutyCycle(0)
        self.motor_2.ChangeDutyCycle(speed)
        self.motor_3.ChangeDutyCycle(0)
        self.motor_4.ChangeDutyCycle(speed)

    def pause(self) -> None:
        """Stop the car
        """
        self.initital()

    def turn_in_moving(self, speed_right: int, speed_left: int) -> None:
        """Seems cannot work.

        Args:
            speed_right (int): motor electrical signal duty cycle for wheels in the left side, from 0 to 100.
            speed_left (int): motor electrical signal duty cycle for wheels in the right side, from 0 to 100.
        """
        self.motor_1.ChangeDutyCycle(speed_right)
        self.motor_2.ChangeDutyCycle(0)
        self.motor_3.ChangeDutyCycle(speed_left)
        self.motor_4.ChangeDutyCycle(0)

    def turn_right_in_place(self, speed: int) -> None:
        """Turn left with the left back wheel as the origin.

        Args:
            speed (int): motor electrical signal duty cycle。
        """
        self.motor_1.ChangeDutyCycle(0)
        self.motor_2.ChangeDutyCycle(speed)
        self.motor_3.ChangeDutyCycle(speed)
        self.motor_4.ChangeDutyCycle(0)

    def turn_left_in_place(self, speed: int) -> None:
        """Turn right with the right back wheel as the origin.

        Args:
            speed (int): motor electrical signal duty cycle。
        """
        self.motor_1.ChangeDutyCycle(speed)
        self.motor_2.ChangeDutyCycle(0)
        self.motor_3.ChangeDutyCycle(0)
        self.motor_4.ChangeDutyCycle(speed)


def test_motor():
    GPIO.cleanup()
    motor = Motor()
    try:
        motor.forward(50)
        time.sleep(2)
        # motor.backword(50)
        # time.sleep(2)
        motor.turn_in_moving(50, 10)
        time.sleep(0.5)
        motor.forward(50)
        time.sleep(2)
        while 1:
            pass

    except KeyboardInterrupt as e:
        motor.stop()
        GPIO.cleanup()