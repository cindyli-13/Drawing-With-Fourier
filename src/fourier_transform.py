import numpy as np
from math import pi, cos, sin, sqrt, atan2


# discrete fourier transform with n harmonics (https://en.wikipedia.org/wiki/Discrete_Fourier_transform)
# returns lists of [amplitude, frequency, phase] and total number of sample points
def dft(f_time_x: list, f_time_y: list, n: int) -> tuple:
    
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
            f_freq.append([sqrt(re**2 + im**2), k * base_freq * 100, atan2(im, re)])    # scale frequency to a viewable value

    return f_freq_x, f_freq_y, N
