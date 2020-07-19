import sys
import cv2
from math import pi

from PyQt5.QtWidgets import QApplication

from plot import MainWindow
from image_processing import get_time_domain_func
from fourier_transform import dft


def main():

    # number of harmonics
    n = 10

    img = cv2.imread('../images/batman.jpg')

    f_time_x, f_time_y = get_time_domain_func(img)
    f_freq_x, f_freq_y, N = dft(f_time_x, f_time_y, n)

    # x values should be pi/2 out of phase
    f_freq_x = list(map(lambda x: [x[0], x[1], x[2]+pi/2], f_freq_x))

    # sort by largest to smallest amplitudes
    f_freq_x.sort(key=(lambda x: x[0]), reverse=True)
    f_freq_y.sort(key=(lambda x: x[0]), reverse=True)
    
    # create plot
    app = QApplication(sys.argv)
    main = MainWindow(60, N, f_freq_x, f_freq_y)
    main.resize(2000, 2000)
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
