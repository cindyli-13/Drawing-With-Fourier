import cv2
import numpy as np
from math import inf, sqrt
from functools import reduce


def get_contour_path(image: np.ndarray) -> list:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blurred, 120, 220)
    ret, thresh = cv2.threshold(canny, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    filtered_contours, to_remove = [], []
    for i, contour in enumerate(contours):

        # remove redundant contours
        if i in to_remove:
            to_remove.remove(i)

        elif cv2.contourArea(contour) > 10:
            contour = np.append(contour, np.array(contour[:10]), axis=0) # append a bit of the beginning points
            filtered_contours.append(contour)

            # add first child contour to remove list
            if hierarchy[0][i][2] != -1:
                to_remove.append(hierarchy[0][i][2])


    # no contours found
    if len(filtered_contours) == 0:
        return []

    # save contour image for reference
    black_img = np.zeros(image.shape)
    cv2.imwrite('../images/results/contours.jpg', cv2.drawContours(black_img, filtered_contours, -1, (0,255,0), 1))

    # order contours for drawability
    # greedy approach: select next contour based on closest point
    ordered_contours = [filtered_contours[0]]
    curr_contour_coords = ordered_contours[0][0]
    del filtered_contours[0]
    closest_contours = [inf, 0] # used for reordering contours (choose first-last contours to be part of shortest contour pair)

    while len(filtered_contours) > 0:
        shortest = [inf, 0, 0, filtered_contours[0]]
        for i, c in enumerate(filtered_contours):
            for j, coord in enumerate(c):
                dist = sqrt((coord[0][0] - curr_contour_coords[0][0])**2 + (coord[0][1] - curr_contour_coords[0][1])**2)
                if dist < shortest[0]:
                    shortest = [dist, i, j, c]
        
        # reorder contour coordinates
        shortest[3] = np.concatenate((shortest[3][shortest[2]:, :, :], shortest[3][:shortest[2], :, :]))

        ordered_contours.append(shortest[3])
        curr_contour_coords = shortest[3][0]
        del filtered_contours[shortest[1]]

        if shortest[0] < closest_contours[0]:
            closest_contours = [shortest[0], len(ordered_contours)-1]

    # reorder contours
    ordered_contours = ordered_contours[closest_contours[1]:] + ordered_contours[:closest_contours[1]]

    # concatenate contours into one large contour path
    ordered_contour = reduce(lambda a,b: np.concatenate((a,b)), ordered_contours)

    return ordered_contour


# separate contour path into width and height coordinates
def separate_coords(contour_path: list) -> tuple:
    return list(map(lambda x: x[0], contour_path)), list(map(lambda x: x[1], contour_path))


def get_time_domain_func(image: np.ndarray) -> tuple:

    contour_path = get_contour_path(image)

    # adjust y values
    max_y = image.shape[1]
    contour_path = list(map(lambda x: [x[0][0], -x[0][1] + max_y], contour_path))

    f_time_x, f_time_y = separate_coords(contour_path)

    return f_time_x, f_time_y
