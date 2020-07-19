import sys
import cv2
from math import pi

from PyQt5.QtWidgets import QApplication

from plot import MainWindow
from image_processing import get_time_domain_func
from fourier_transform import dft_complex


def main():

    # parameters to tweak
    n = 100
    drawing_speed = 100
    fps = 60                # this one doesn't seem to have an effect on anything...
    window_size = 2000

    img = cv2.imread('../images/batman.jpg')

    f_time_x, f_time_y = get_time_domain_func(img)
    f_freq, N = dft_complex(f_time_x, f_time_y, n)

    # sort by largest to smallest amplitudes
    f_freq.sort(key=(lambda x: x[0]), reverse=True)
    
    # create plot
    app = QApplication(sys.argv)
    main = MainWindow(fps, N, drawing_speed, f_freq)
    main.resize(window_size, window_size)
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
