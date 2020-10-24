import time
import logging

from threading import Thread

from web import app
from plugins.infrared import test_infrared_sensor

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main():
    flasky = Thread(target=app.run, kwargs=({
        'host': '0.0.0.0',
        'port': '8080',
        'debug': False,
        'threaded': True,
    }))
    flasky.start()

    test_infrared_sensor()


if __name__ == "__main__":
    main()
