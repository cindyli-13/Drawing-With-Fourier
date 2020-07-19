import numpy as np
from math import pi, cos, sin, sqrt, atan2


# discrete fourier transform with n harmonics (https://en.wikipedia.org/wiki/Discrete_Fourier_transform)
# returns lists of [amplitude, frequency, phase] and total number of sample points
def dft(f_time_x: list, f_time_y: list, n: int) -> tuple:
    
    f_freq_x, f_freq_y = [], []

    N = len(f_time_x)
    base_freq = 1/N

    for k in range(min(n, N)):

        for f_time, f_freq in [(f_time_x, f_freq_x), (f_time_y, f_freq_y)]:
            re = 0
            im = 0
            for t, x_in in enumerate(f_time):
                theta = 2*pi*k*t/N
                re += x_in * cos(theta)
                im -= x_in * sin(theta)
            re /= N
            im /= N
            f_freq.append([sqrt(re**2 + im**2), k * base_freq, atan2(im, re)])    # scale frequency to a viewable value

    return f_freq_x, f_freq_y, N


# dft with complex inputs (to capture x and y coords in one epicycle chain)
def dft_complex(f_time_x: list, f_time_y: list, n: int) -> tuple:
    
    complex_inputs = []
    for i in range(len(f_time_x)):
        complex_inputs.append(complex(f_time_x[i], f_time_y[i]))
    f_freq = []

    N = len(complex_inputs)
    base_freq = 1/N

    for k in range(-min(n, N)//2, min(n, N)//2):
        c_out = complex(0,0)
        for t, c_in in enumerate(complex_inputs):
            theta = 2*pi*k*t/N
            c_out += c_in * (cos(theta) - complex(0,1) * sin(theta))
        c_out /= N
        f_freq.append([abs(c_out), k * base_freq, atan2(c_out.imag, c_out.real)])    # scale frequency to a viewable value

    return f_freq, N
