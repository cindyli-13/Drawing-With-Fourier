import cv2
import numpy as np
from matplotlib import pyplot as plt


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
