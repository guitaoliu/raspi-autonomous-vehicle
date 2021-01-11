import cv2
from numpy import ndarray


def convert_jpeg(img: ndarray):
    _, jpeg = cv2.imencode(".jpeg", img)
    return jpeg
