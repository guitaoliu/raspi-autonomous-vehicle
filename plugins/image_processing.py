import cv2
from numpy import ndarray
import numpy as np
from config import CarStatus
from typing import Tuple


def processing(img: ndarray, lines: int = 4) -> Tuple:
    img = cv2.blur(img, (5, 5))
    _, _, img_red = cv2.split(img)
    _, dst = cv2.threshold(img_red, 20, 255, cv2.THRESH_BINARY)

    img_gray = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)
    return img_red, dst, img_gray


def strategy(img: ndarray) -> CarStatus:
    height, width = img.shape
    bi = np.ones((height, width))
    black_position = []

    # 每行只保留第一个黑色块
    for i in range(0, height):
        for j in range(0, width):
            if img[i][j] == 0:
                bi[i][j] = 0.
                black_position.append(j)
                break

    bias = np.average(black_position) - width/2
    if bias > 0.1 * width:
        return CarStatus.RIGHT
    elif bias < -0.1*width:
        return CarStatus.LEFT
    else:
        return CarStatus.FORWARD

