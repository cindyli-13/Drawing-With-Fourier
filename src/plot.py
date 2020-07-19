from time import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPen
from pyqtgraph import PlotWidget
import pyqtgraph as pg

from epicycles import EpicycleSeries, freq_to_epicycles


class MainWindow(QtWidgets.QMainWindow):

    # period in seconds
    def __init__(self, fps: float, period_in_frames: int, f_freq_x: list, f_freq_y: list, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.setWindowTitle("Drawing with Fourier")

        self.period_in_frames = period_in_frames
        self.fps = fps

        # black background
        self.graphWidget.setBackground('k')

        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setXRange(0, 100, padding=0)
        self.graphWidget.setYRange(0, 100, padding=0)
        
        # pen for lines connecting circle centers to circle points
        pen = pg.mkPen(color='w', width=0.5)

        # create epicycle series for x and y functions
        self.epicycle_series_x = freq_to_epicycles(f_freq_x, 0, 0)
        self.epicycle_series_y = freq_to_epicycles(f_freq_y, 0, 0)

        # points on circles
        self.points = self.graphWidget.plot([], [], pen=None, symbol='o', symbolBrush='w', symbolSize=3)
        
        # lines connecting circle centers to circle points
        self.lines_x, self.lines_y = [], []
        for i in range(self.epicycle_series_x.n):
            self.lines_x.append(self.graphWidget.plot([], [], pen=pen))
        for i in range(self.epicycle_series_y.n):
            self.lines_y.append(self.graphWidget.plot([], [], pen=pen))

        # points on sketch
        pen = pg.mkPen(color='w', width=1)
        self.sketch_data_x, self.sketch_data_y = [], []
        self.sketch = self.graphWidget.plot([], [], pen=pen)

        # line x and y
        pen = pg.mkPen(color='b', width=0.5)
        self.line_x = self.graphWidget.plot([], [], pen=pen)
        self.line_y = self.graphWidget.plot([], [], pen=pen)

        # sketch point
        self.sketch_point = self.graphWidget.plot([], [], pen=None, symbol='o', symbolBrush='w', symbolSize=5)

        # time reference (seconds)
        self.init_time = time()
        self.prev_time = 0

        # set up timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1/fps)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def update(self):
        t = time() - self.init_time

        self.epicycle_series_x.update(t)
        self.epicycle_series_y.update(t)

        # points on circles
        self.points.setData(self.epicycle_series_x.centers_x + self.epicycle_series_y.centers_x, 
                            self.epicycle_series_x.centers_y + self.epicycle_series_y.centers_y)
        
        # lines connecting circle centers to circle points
        for i, line in enumerate(self.lines_x):
            line.setData([self.epicycle_series_x.centers_x[i], self.epicycle_series_x.centers_x[i+1]],
                         [self.epicycle_series_x.centers_y[i], self.epicycle_series_x.centers_y[i+1]])
        for i, line in enumerate(self.lines_y):
            line.setData([self.epicycle_series_y.centers_x[i], self.epicycle_series_y.centers_x[i+1]],
                         [self.epicycle_series_y.centers_y[i], self.epicycle_series_y.centers_y[i+1]])

        x = self.epicycle_series_y.centers_x[-1]
        y = self.epicycle_series_x.centers_y[-1]

        # time domain lines
        self.line_x.setData([self.epicycle_series_x.centers_x[-1], x], [self.epicycle_series_x.centers_y[-1], self.epicycle_series_x.centers_y[-1]])
        self.line_y.setData([self.epicycle_series_y.centers_x[-1], self.epicycle_series_y.centers_x[-1]], [y, self.epicycle_series_y.centers_y[-1]])

        # points on sketch
        if self.epicycle_series_x.n > 0 and len(self.sketch_data_x) < self.period_in_frames:
            self.sketch_data_x.append(x)
            self.sketch_data_y.append(y)
            self.sketch.setData(self.sketch_data_x, self.sketch_data_y)
        
        # sketch point
        self.sketch_point.setData([x], [y])

        # update previous time
        self.prev_time = time() - self.init_time
