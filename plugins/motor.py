import time

import RPi.GPIO as GPIO

from config import Config


class Motor:

    def __init__(self):
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
        self.motor_1.start(0)
        self.motor_2.start(0)
        self.motor_3.start(0)
        self.motor_4.start(0)

    def stop(self) -> None:
        self.motor_1.stop()
        self.motor_2.stop()
        self.motor_3.stop()
        self.motor_4.stop()

    def forward(self, speed: int) -> None:
        self.motor_1.ChangeDutyCycle(speed)
        self.motor_2.ChangeDutyCycle(0)
        self.motor_3.ChangeDutyCycle(speed)
        self.motor_4.ChangeDutyCycle(0)

    def backword(self, speed: int) -> None:
        self.motor_1.ChangeDutyCycle(0)
        self.motor_2.ChangeDutyCycle(speed)
        self.motor_3.ChangeDutyCycle(0)
        self.motor_4.ChangeDutyCycle(speed)

    def pause(self) -> None:
        self.initital()

    def turn_in_moving(self, speed_left: int, speed_right: int) -> None:
        self.motor_1.ChangeDutyCycle(speed_left)
        self.motor_2.ChangeDutyCycle(0)
        self.motor_3.ChangeDutyCycle(speed_right)
        self.motor_4.ChangeDutyCycle(0)

    def turn_left_in_place(self, speed: int) -> None:
        self.motor_1.ChangeDutyCycle(0)
        self.motor_2.ChangeDutyCycle(speed)
        self.motor_3.ChangeDutyCycle(speed)
        self.motor_4.ChangeDutyCycle(0)

    def turn_right_in_place(self, speed: int) -> None:
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
        motor.backword(50)
        time.sleep(2)
        motor.turn_left_in_place(50)
        time.sleep(2)
        motor.turn_right_in_place(50)
        time.sleep(2)
        motor.turn_in_moving(30, 50)
        time.sleep(2)
        while 1:
            pass

    except KeyboardInterrupt as e:
        motor.stop()
        GPIO.cleanup()
