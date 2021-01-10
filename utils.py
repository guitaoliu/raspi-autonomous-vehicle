from threading import Thread

import cv2
from numpy import ndarray

from web import app


def convert_jpeg(img: ndarray):
    _, jpeg = cv2.imencode(".jpeg", img)
    return jpeg


def start_web():
    Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port="8080",
            debug=False,
            threaded=True,
        )
    ).start()
