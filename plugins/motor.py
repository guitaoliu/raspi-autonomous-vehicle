import RPi.GPIO as GPIO

from config import Config


class Motor:

    def __init__(self):
        GPIO.setup(Config.MOTOR_1_GPIO_BCM, GPIO.OUT)
        GPIO.setup(Config.MOTOR_2_GPIO_BCM, GPIO.OUT)
        GPIO.setup(Config.MOTOR_3_GPIO_BCM, GPIO.OUT)
        GPIO.setup(Config.MOTOR_4_GPIO_BCM, GPIO.OUT)

        self.motor_1 = GPIO.PWM(Config.MOTOR_1_GPIO_BCM, 500)
        self.motor_2 = GPIO.PWM(Config.MOTOR_1_GPIO_BCM, 500)
        self.motor_3 = GPIO.PWM(Config.MOTOR_1_GPIO_BCM, 500)
        self.motor_4 = GPIO.PWM(Config.MOTOR_1_GPIO_BCM, 500)

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
        self.motor_2.ChangeDutyCycle(speed)
        self.motor_3.ChangeDutyCycle(speed)
        self.motor_4.ChangeDutyCycle(speed)

    def pause(self) -> None:
        self.initital()

    def turn_left(self):
        pass

    def turn_right(self):
        pass
