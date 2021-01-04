from typing import List, Tuple

import cv2
import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt

from config import CarStatus, PathType


def get_pts1(img: ndarray) -> ndarray:
    plt.imshow(img)
    pts1 = plt.ginput(n=-1, timeout=0)
    return pts1.astype('float32')


def perspective_transform(img: ndarray) -> ndarray:
    # PerspectiveTransform
    # manually select pts1
    pts1 = get_pts1(img)
    pts2 = np.float32([[200, 200], [400, 200], [400, 400], [200, 400]])
    transform_matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return transform_matrix


def processing(img: ndarray, transform_matrix: ndarray, lines: int = 4) -> Tuple:
    # output size is changed to (600,600)
    img = cv2.warpPerspective(img, transform_matrix, (600, 600))
    img = cv2.blur(img, (5, 5))
    _, _, img_red = cv2.split(img)
    # Filtering background noise
    for i, row in zip(range(img_red.shape[0]), img_red):
        if np.average(row) < 100:
            img_red[i, :] = 255
    _, dst = cv2.threshold(img_red, 80, 255, cv2.THRESH_BINARY)
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
            if bw_edge.min() < wb_edge.max() :
                scenario_list.append(PathType.BothSides)
            else:
                scenario_list.append(PathType.OneSide)
        elif len(bw_edge) > 0 or len(wb_edge) > 0:
            scenario_list.append(PathType.OneSide)
        else:
            scenario_list.append(PathType.NonSide)

    return scenario_list


def both_sides_strategy(img: ndarray, scenario_list: List[PathType]) -> CarStatus:
    height, width = img.shape
    center_position = []

    # 每行只保留俩个个黑色块
    for i, scenario in zip(range(height), scenario_list):
        if scenario == PathType.BothSides:
            left_black = None
            right_black = None
            for j in range(width):
                if img[i][j] == 0:
                    left_black = j
                    break
            for j in range(width - 1, -1, -1):
                if img[i][j] == 0:
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


def one_side_strategy(img: ndarray, scenario_list: List[PathType]) -> CarStatus:
    height, width = img.shape
    black_position = []

    # 每行只保留第一个黑色块
    for i, scenario in zip(range(height), scenario_list):
        if scenario == PathType.OneSide:
            for j in range(width):
                if img[i][j] == 0:
                    black_position.append(j)
                    break

    # lead the car with line slope
    # line slope is defined as average of black_positions' difference
    diff = np.diff(np.array(black_position))
    if np.sum(diff > 0) - np.sum(diff < 0) > np.sum(diff == 0):
        slope = 1
    elif np.sum(diff < 0) - np.sum(diff > 0) > np.sum(diff == 0):
        slope = -1
    else:
        slope = 0
    if slope > 0:
        return CarStatus.LEFT
    elif slope < 0:
        return CarStatus.RIGHT
    else:
        return CarStatus.FORWARD


def strategy(img: ndarray, scenario_list: List[PathType]) -> CarStatus:
    height, width = img.shape

    # whole image scenario is defined by the scenario of rows
    if scenario_list.count(PathType.BothSides) > 0.2 * height:
        whole_scenario = PathType.BothSides
    elif scenario_list.count(PathType.OneSide) > 0.2 * height:
        whole_scenario = PathType.OneSide
    else:
        whole_scenario = PathType.NonSide

    if whole_scenario == PathType.BothSides:
        return both_sides_strategy(img, scenario_list)
    elif whole_scenario == PathType.OneSide:
        return one_side_strategy(img, scenario_list)
    else:
        return CarStatus.FORWARD
