import numpy as np
from math import pi, cos, sin, sqrt, atan2

from image_processing import get_contour_path


# separate contour path into x and y values
def separate_coords(contour_path: list) -> tuple:
    return list(map(lambda x: x[0], contour_path)), list(map(lambda x: x[1], contour_path))

# TODO - change input params from image to f_time
# discrete fourier transform with n harmonics (https://en.wikipedia.org/wiki/Discrete_Fourier_transform)
# returns lists of [amplitude, frequency, phase] and total number of sample points
def dft(img: np.ndarray, n: int) -> tuple:
    if n <= 0:
        return []

    # get image contour
    contour_path = get_contour_path(img)

    # adjust y values
    max_y = img.shape[1]
    contour_path = list(map(lambda x: [x[0][0], -x[0][1] + max_y], contour_path))

    f_time_y, f_time_x = separate_coords(contour_path)
    f_freq_x, f_freq_y = [], []

    N = len(f_time_x)
    base_freq = 1/N

    for k in range(n):

        for f_time, f_freq in [(f_time_x, f_freq_x), (f_time_y, f_freq_y)]:
            re = 0
            im = 0
            for t, x_in in enumerate(f_time):
                theta = 2*pi*k*t/N
                re += x_in * cos(theta)
                im -= x_in * sin(theta)
            re /= N
            im /= N
            f_freq.append([sqrt(re**2 + im**2), k*base_freq * 100, atan2(im, re)])

    return f_freq_x, f_freq_y, N
