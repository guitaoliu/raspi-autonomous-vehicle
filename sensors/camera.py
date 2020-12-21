import threading
import time

import cv2
import numpy as np
import picamera
from picamera.array import PiRGBArray


class Camera:
    def __init__(self) -> None:
        self.ca = picamera.PiCamera()
        self.ca.resolution = (640, 480)
        self.ca.framerate = 32

        self.array = PiRGBArray(self.ca, size=(640, 480))
        self.array_np = None
        self.frame = None
        self.ca.start_preview()

        time.sleep(1)
        threading.Thread(target=lambda: self.gen()).start()

    def gen(self):
        for r in self.ca.capture_continuous(self.array, "bgr", use_video_port=True):
            self.array_np = np.copy(r.array)
            self.jpeg()
            self.array.truncate(size=0)

    def jpeg(self):
        _, buf = cv2.imencode(".jpeg", self.array_np)
        self.frame = buf
