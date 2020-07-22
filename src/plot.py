from time import time
import numpy as np
import cv2

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPen
from pyqtgraph import PlotWidget
import pyqtgraph as pg

from image_processing import get_time_domain_func
from fourier_transform import dft_complex
from epicycles import EpicycleChain, freq_to_epicycles


class MainWindow(QMainWindow):

    def __init__(self, img: np.ndarray, n: int, drawing_speed: float, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graph = pg.PlotWidget()
        self.setCentralWidget(self.graph)
        self.setWindowTitle("Drawing with Fourier")

        self.graph.setBackground((15,45,90))

        self.graph.showGrid(x=True, y=True)
        self.graph.setXRange(0, 700, padding=0)
        self.graph.setYRange(0, 700, padding=0)

        # convert image to frequency function
        f_time_x, f_time_y = get_time_domain_func(img)
        f_freq, N = dft_complex(f_time_x, f_time_y, n)

        # sort by largest to smallest amplitudes
        f_freq.sort(key=(lambda x: x[0]), reverse=True)

        # create epicycle chain for x and y functions
        self.epicycle_chain = freq_to_epicycles(f_freq, 0, 0, drawing_speed)

        self.period_in_frames = N
        self.fps = 60

        # points on circles
        self.points = self.graph.plot([], [], pen=None, symbol='o', symbolBrush='w', symbolSize=2)
        
        # lines connecting circle centers to circle points and points on circle circumferences
        self.lines = []
        self.circumference_points = []

        for i in range(self.epicycle_chain.n):
            self.lines.append(self.graph.plot([], [], pen=pg.mkPen(color=(160,200,255), width=0.5)))
            self.circumference_points.append(self.graph.plot([], [], pen=pg.mkPen(color=(140,180,240), width=0.2)))

        # points on sketch
        self.sketch_data_x, self.sketch_data_y = [], []
        self.sketch = self.graph.plot([], [], pen=pg.mkPen(color='w', width=1))

        # sketch point
        self.sketch_point = self.graph.plot([], [], pen=None, symbol='o', symbolBrush='w', symbolSize=5)

        # time reference (seconds)
        self.init_time = time()

        # set up timer
        self.timer = QTimer()
        self.timer.setInterval(1/self.fps)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def update(self):

        # no need to update if no data
        if self.epicycle_chain.n == 0:
            return

        t = time() - self.init_time

        self.epicycle_chain.update(t)

        # points on circles
        self.points.setData(self.epicycle_chain.centers_x, self.epicycle_chain.centers_y)
        
        # lines connecting circle centers to circle points
        for i, line in enumerate(self.lines):
            line.setData([self.epicycle_chain.centers_x[i], self.epicycle_chain.centers_x[i+1]],
                         [self.epicycle_chain.centers_y[i], self.epicycle_chain.centers_y[i+1]])

        # points on circle circumferences
        for i, circle in enumerate(self.circumference_points[:-1]):
            circle.setData(self.epicycle_chain.circumference_coords_x[i+1], self.epicycle_chain.circumference_coords_y[i+1])
        
        x = self.epicycle_chain.centers_x[-1]
        y = self.epicycle_chain.centers_y[-1]

        # points on sketch
        if self.epicycle_chain.n > 0 and len(self.sketch_data_x) < self.period_in_frames:
            self.sketch_data_x.append(x)
            self.sketch_data_y.append(y)
            self.sketch.setData(self.sketch_data_x, self.sketch_data_y)
        
        # sketch point
        self.sketch_point.setData([x], [y])
