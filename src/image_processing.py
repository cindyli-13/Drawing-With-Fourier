import cv2
import numpy as np
from math import inf, sqrt
from functools import reduce


def get_contour_path(image: np.ndarray) -> list:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3,3), 0)
    canny = cv2.Canny(blurred, 150, 220)
    ret, thresh = cv2.threshold(canny, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    filtered_contours = []
    for i, contour in enumerate(contours):
        if cv2.contourArea(contour) > 5:
            contour = np.append(contour, np.array([contour[0]]), axis=0)
            filtered_contours.append(contour)

    # no contours found
    if len(filtered_contours) == 0:
        return []

    # order contours for drawability
    # greedy approach: find next closest contour based on contour's starting point
    ordered_contours = [filtered_contours[0]]
    del filtered_contours[0]

    curr_contour_coords = ordered_contours[0][0]

    while len(filtered_contours) > 1:
        shortest = [inf, 0, filtered_contours[0]]
        for i, c in enumerate(filtered_contours):
            dist = sqrt((c[0][0][0] - curr_contour_coords[0][0])**2 + (c[0][0][1] - curr_contour_coords[0][1])**2)
            if dist < shortest[0]:
                shortest = [dist, i, c]
        ordered_contours.append(shortest[2])
        curr_contour_coords = shortest[2][0]
        del filtered_contours[shortest[1]]

    ordered_contours.append(filtered_contours[0])

    # concatenate contours into one large contour path
    ordered_contour = reduce(lambda a,b: np.concatenate((a,b)), ordered_contours)

    return ordered_contour


# separate contour path into width and height coordinates
def separate_coords(contour_path: list) -> tuple:
    return list(map(lambda x: x[0], contour_path)), list(map(lambda x: x[1], contour_path))


# returns f_time_x, f_time_y
def get_time_domain_func(image: np.ndarray) -> tuple:

    contour_path = get_contour_path(image)

    # adjust y values
    max_y = image.shape[1]
    contour_path = list(map(lambda x: [x[0][0], -x[0][1] + max_y], contour_path))

    f_time_x, f_time_y = separate_coords(contour_path)

    return f_time_x, f_time_y
