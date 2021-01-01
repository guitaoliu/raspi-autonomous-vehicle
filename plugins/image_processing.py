import cv2
from numpy import ndarray
import numpy as np
from config import CarStatus, PathType
from typing import Tuple, List


def processing(img: ndarray, lines: int = 4) -> Tuple:
    img = cv2.blur(img, (5, 5))
    _, _, img_red = cv2.split(img)
    _, dst = cv2.threshold(img_red, 20, 255, cv2.THRESH_BINARY)

    img_gray = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)
    return img_red, dst, img_gray

def scenraio_analyse(img: ndarray) -> List[PathType]:
    height, width = img.shape
    diff_img = np.diff(img)
    scenraio_list = []

    # identify number of edges according to positions of bw_edge and wb_edge 
    for row in diff_img:
        bw_edge = np.argwhere(row>0).reshape(-1)
        wb_edge = np.argwhere(row<0).reshape(-1)
        if len(bw_edge)>0 and len(wb_edge)>0:
            if bw_edge.min() < wb_edge.max():
                scenraio_list.append(PathType.BothSides)
            else:
                scenraio_list.append(PathType.OneSide)
        elif len(bw_edge)>0 or len(wb_edge)>0:
            scenraio_list.append(PathType.OneSide)
        else:
            scenraio_list.append(PathType.NonSide)
    
    return scenraio_list
    # whole image scenraio is defined by the 
    if scenraio_list.count() > 0.2 * height:
        return PathType.BothSides
    elif onesides_count > 0.1 * height:
        return PathType.OneSide
    else:
        return PathType.NonSide

def BothSides_strategy(img: ndarray, scenraio_list: List[PathType]) -> CarStatus:
    height, width = img.shape
    center_position = []

    # 每行只保留俩个个黑色块
    for i, scenraio in zip(range(0, height), scenraio_list):
        if scenraio==PathType.BothSides:
            left_black = None
            right_bleck = None
            for j in range(0, width):
                if img[i][j] == 0:
                    bi[i][j] = 0.
                    left_black=j
                    break
            for j in range(width, 0, -1):
                if img[i][j] == 0:
                    bi[i][j] = 0.
                    right_bleck=j
                    break
            center_position.append((left_black + right_bleck) / 2)
    
    bias = np.average(center_position) - width/2
    if bias > 0.1 * width:
        return CarStatus.RIGHT
    elif bias < -0.1*width:
        return CarStatus.LEFT
    else:
        return CarStatus.FORWARD

def OneSide_strategy(img: ndarray, scenraio_list: List[PathType]) -> CarStatus:
    height, width = img.shape
    black_position = []

    # 每行只保留第一个黑色块
    for i in range(0, height):
        if scenraio==PathType.OneSide:
        for j in range(0, width):
            if img[i][j] == 0:
                bi[i][j] = 0.
                black_position.append(j)
                break
    
    # lead the car with line slope
    # line slope is defined as average of black_positions' difference 
    diff = np.diff(np.array(black_position))
    slope = np.average(diff)
    if slope > 0:
        return CarStatus.LEFT
    elif slope < 0:
        return CarStatus.RIGHT
    else:
        return CarStatus.FORWARD

def strategy(img: ndarray, scenraio_list: List[PathType]) -> CarStatus:
    height, width = img.shape
    bi = np.ones((height, width))
    black_position = []
    
    # whole image scenraio is defined by the scenraio of rows
    if scenraio_list.count(PathType.BothSides) > 0.3 * height:
        whole_scenraio = PathType.BothSides
    elif scenraio_list.count(PathType.OneSide) > 0.3 * height:
        whole_scenraio = PathType.OneSide
    else:
        whole_scenraio = PathType.NonSide

    if whole_scenraio==PathType.BothSides:
        return BothSides_strategy(img, scenraio_list)
    elif whole_scenraio==PathType.OneSide:
        eturn OneSide_strategy(img, scenraio_list)
    else:
        return CarStatus.FORWARD
