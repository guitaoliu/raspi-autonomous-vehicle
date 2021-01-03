from typing import List, Tuple

import cv2
import numpy as np
from numpy import ndarray

from config import CarStatus, PathType


def processing(img: ndarray, lines: int = 4) -> Tuple:
    img = cv2.blur(img, (5, 5))
    _, _, img_red = cv2.split(img)
    _, dst = cv2.threshold(img_red, 20, 255, cv2.THRESH_BINARY)

    img_gray = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)
    return img_red, dst, img_gray


def scenario_analyse(img: ndarray) -> List[PathType]:
    height, width = img.shape
    diff_img = np.diff(img.astype(np.float32))
    scenario_list = []

    # identify number of edges according to positions of bw_edge and wb_edge
    for row in diff_img:
        bw_edge = np.argwhere(row > 0).reshape(-1)
        wb_edge = np.argwhere(row < 0).reshape(-1)
        if len(bw_edge) > 0 and len(wb_edge) > 0:
            if bw_edge.min() < wb_edge.max():
                scenario_list.append(PathType.BothSides)
            else:
                scenario_list.append(PathType.OneSide)
        elif len(bw_edge) > 0 or len(wb_edge) > 0:
            scenario_list.append(PathType.OneSide)
        else:
            scenario_list.append(PathType.NonSide)

    return scenario_list


def both_sides_strategy(
    img: ndarray, scenario_list: List[PathType], bi: ndarray
) -> CarStatus:
    height, width = img.shape
    center_position = []

    # 每行只保留俩个个黑色块
    for i, scenario in zip(range(height), scenario_list):
        if scenario == PathType.BothSides:
            left_black = None
            right_black = None
            for j in range(width):
                if img[i][j] == 0:
                    bi[i][j] = 0.0
                    left_black = j
                    break
            for j in range(width-1, -1, -1):
                if img[i][j] == 0:
                    bi[i][j] = 0.0
                    right_black = j
                    break
            center_position.append((left_black + right_black) / 2)

    bias = np.average(center_position) - width / 2
    if bias > 0.1 * width:
        return CarStatus.RIGHT
    elif bias < -0.1 * width:
        return CarStatus.LEFT
    else:
        return CarStatus.FORWARD


def one_side_strategy(
    img: ndarray, scenario_list: List[PathType], bi: ndarray
) -> CarStatus:
    height, width = img.shape
    black_position = []

    # 每行只保留第一个黑色块
    for i, scenario in zip(range(height), scenario_list):
        if scenario == PathType.OneSide:
            for j in range(width):
                if img[i][j] == 0:
                    bi[i][j] = 0.0
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


def strategy(img: ndarray, scenario_list: List[PathType]) -> CarStatus:
    height, width = img.shape
    bi = np.ones((height, width))

    # whole image scenario is defined by the scenario of rows
    if scenario_list.count(PathType.BothSides) > 0.3 * height:
        whole_scenario = PathType.BothSides
    elif scenario_list.count(PathType.OneSide) > 0.3 * height:
        whole_scenario = PathType.OneSide
    else:
        whole_scenario = PathType.NonSide

    if whole_scenario == PathType.BothSides:
        return both_sides_strategy(img, scenario_list, bi)
    elif whole_scenario == PathType.OneSide:
        return one_side_strategy(img, scenario_list, bi)
    else:
        return CarStatus.FORWARD
