import io
import threading
import time

import picamera

from core.object_detect import ObjectDetect

detection = ObjectDetect()


class Camera(object):
    thread = None
    frame = None
    last_access = 0

    def initialize(self) -> None:
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    def get_detected_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return detection.gen_bytes(self.frame)

    @classmethod
    def _thread(cls) -> None:
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (640, 480)

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, "jpeg", use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
