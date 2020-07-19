from math import pi, cos, sin, sqrt, atan2


# discrete fourier transform with n harmonics (https://en.wikipedia.org/wiki/Discrete_Fourier_transform)
# returns lists of [amplitude, frequency, phase] and total number of sample points
def dft(f_time_x: list, f_time_y: list, n: int) -> tuple:
    
    N = len(f_time_x)

    f_freq_x, f_freq_y = [], []
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
            f_freq.append([sqrt(re**2 + im**2), k, atan2(im, re)])

    return f_freq_x, f_freq_y, N


# dft with complex inputs (to capture x and y coords in one epicycle chain)
def dft_complex(f_time_x: list, f_time_y: list, n: int) -> tuple:
    
    # convert (x,y) coordinates to complex numbers
    complex_inputs = []
    for x, y in zip(f_time_x, f_time_y):
        complex_inputs.append(complex(x, y))

    N = len(complex_inputs)

    f_freq = []
    for k in range(-min(n, N)//2, min(n, N)//2):
        c_out = complex(0,0)
        for t, c_in in enumerate(complex_inputs):
            theta = 2*pi*k*t/N
            c_out += c_in * (cos(theta) - complex(0,1) * sin(theta))
        c_out /= N
        f_freq.append([abs(c_out), k, atan2(c_out.imag, c_out.real)])

    return f_freq, N
