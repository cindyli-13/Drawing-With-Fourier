import sys
import os
import cv2
from math import pi

from PyQt5.QtWidgets import QApplication

from plot import MainWindow

DEFAULT_N               = 100
DEFAULT_DRAWING_SPEED   = 0.01
DEFAULT_WINDOW_SIZE     = 2000


def print_usage():
    print('\nUsage: python main.py PATH_TO_IMAGE [OPTIONS]\n\n \
    Options:\n \
      --n=NUMBER_OF_HARMONICS     default is {}\n \
      --speed=DRAWING_SPEED       default is {}\n \
      --size=WINDOW_SIZE          default is {}\n \
      --help                      displays this text'
      .format(DEFAULT_N, DEFAULT_DRAWING_SPEED, DEFAULT_WINDOW_SIZE))

def main():

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(-1)

    # default parameters
    n = DEFAULT_N
    drawing_speed = DEFAULT_DRAWING_SPEED
    window_size = DEFAULT_WINDOW_SIZE

    # parse arguments
    for arg in sys.argv[1:]:
        if arg.startswith('--n='):
            n = int(arg[4:])
        elif arg.startswith('--speed='):
            drawing_speed = float(arg[8:])
        elif arg.startswith('--size='):
            window_size = int(arg[7:])
        elif arg == '--help':
            print_usage()
            sys.exit(0)

    img_path = sys.argv[1]
    if not os.path.exists(img_path):
        print('Error: file \'{}\' does not exist'.format(img_path))
        sys.exit(-1)

    img = cv2.imread(img_path)

    print('\nDrawing:', img_path)
    print(' - n =', n)
    print(' - Drawing speed =', drawing_speed)
    print(' - Window size =', window_size)
    
    # create plot
    app = QApplication([])
    main = MainWindow(img, n, drawing_speed)
    main.resize(window_size, window_size)
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
