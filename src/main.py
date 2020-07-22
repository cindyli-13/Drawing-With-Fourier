import sys
import cv2
from math import pi

from PyQt5.QtWidgets import QApplication

from plot import MainWindow


def main():

    # parameters to tweak
    n = 500
    drawing_speed = 0.002
    window_size = 2000

    img = cv2.imread('../images/Cindy_google.jpg')
    
    # create plot
    app = QApplication(sys.argv)
    main = MainWindow(img, n, drawing_speed)
    main.resize(window_size, window_size)
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
