import cv2
import numpy as np


def get_contour_path(image: np.ndarray) -> list:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blurred, 150, 220)
    ret, thresh = cv2.threshold(canny, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # TODO
    filtered_contours = []
    for contour in contours:
        if cv2.contourArea(contour) > 5:
            filtered_contours.append(contour)

    # sort by order of descending contour area
    filtered_contours.sort(key=cv2.contourArea, reverse=True)

    return filtered_contours[0] if len(filtered_contours) > 0 else []


# separate contour path into x and y values
def separate_coords(contour_path: list) -> tuple:
    return list(map(lambda x: x[0], contour_path)), list(map(lambda x: x[1], contour_path))


# returns f_time_x, f_time_y
def get_time_domain_func(image: np.ndarray) -> tuple:

    contour_path = get_contour_path(image)

    # adjust y values
    max_y = image.shape[1]
    contour_path = list(map(lambda x: [x[0][0], -x[0][1] + max_y], contour_path))

    f_time_y, f_time_x = separate_coords(contour_path)

    return f_time_x, f_time_y
