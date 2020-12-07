import logging
import time
from threading import Thread

from core.car import Car
from web import app
from core.object_detect import ObjectDetect

logger = logging.getLogger(__name__)


def main():
    Thread(target=app.run, kwargs=({
        'host': '0.0.0.0',
        'port': '8080',
        'debug': False,
        'threaded': True,
    })).start()
    car = Car()
    # Thread(target=car.loop).start()
    #
    # time.sleep(0.5)
    # car.update_move_status(car.status.LEFT)
    # time.sleep(0.5)
    # car.update_move_status(car.status.STOP)


if __name__ == "__main__":
    main()
