import time
import logging

from threading import Thread

from web import app
from plugins.infrared import test_infrared_sensor
from plugins.motor import test_motor
from plugins.ultrasound import test_ultrasoud

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main():
    # flasky = Thread(target=app.run, kwargs=({
    #     'host': '0.0.0.0',
    #     'port': '8080',
    #     'debug': False,
    #     'threaded': True,
    # }))
    # flasky.start()
    # test_motor()
    # test_infrared_sensor()
    test_ultrasoud()


if __name__ == "__main__":
    main()
