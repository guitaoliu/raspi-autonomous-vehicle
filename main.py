import logging
from threading import Thread

import RPi.GPIO as GPIO

from core import car
from web import app

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():
    Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port="8080",
            debug=False,
            threaded=True,
        )
    ).start()
    with car as c:
        try:
            c.run()
        except KeyboardInterrupt:
            c.camera.close()
            GPIO.cleanup()


if __name__ == "__main__":
    main()
