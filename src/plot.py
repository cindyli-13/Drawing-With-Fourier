from time import time

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPen
from pyqtgraph import PlotWidget
import pyqtgraph as pg

from epicycles import EpicycleChain, freq_to_epicycles


class MainWindow(QMainWindow):

    def __init__(self, fps: float, period_in_frames: int, f_freq_x: list, f_freq_y: list, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.setWindowTitle("Drawing with Fourier")

        self.period_in_frames = period_in_frames
        self.fps = fps

        self.graphWidget.setBackground((15,45,90))

        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setXRange(0, 100, padding=0)
        self.graphWidget.setYRange(0, 100, padding=0)

        # create epicycle chain for x and y functions
        self.epicycle_chain_x = freq_to_epicycles(f_freq_x, 0, 0)
        self.epicycle_chain_y = freq_to_epicycles(f_freq_y, 0, 0)

        # points on circles
        self.points = self.graphWidget.plot([], [], pen=None, symbol='o', symbolBrush='w', symbolSize=2)
        
        # lines connecting circle centers to circle points and points on circle circumferences
        pen1 = pg.mkPen(color=(160,200,255), width=0.5)
        pen2 = pg.mkPen(color=(140,180,240), width=0.2)

        self.lines_x, self.lines_y = [], []
        self.circumference_points_x, self.circumference_points_y = [], []

        for i in range(self.epicycle_chain_x.n):
            self.lines_x.append(self.graphWidget.plot([], [], pen=pen1))
            self.circumference_points_x.append(self.graphWidget.plot([], [], pen=pen2)) 

        for i in range(self.epicycle_chain_y.n):
            self.lines_y.append(self.graphWidget.plot([], [], pen=pen1))
            self.circumference_points_y.append(self.graphWidget.plot([], [], pen=pen2)) 

        # points on sketch
        pen = pg.mkPen(color='w', width=1)
        self.sketch_data_x, self.sketch_data_y = [], []
        self.sketch = self.graphWidget.plot([], [], pen=pen)

        # line x and y
        pen = pg.mkPen(color=(200,220,255), width=0.5)
        self.line_x = self.graphWidget.plot([], [], pen=pen)
        self.line_y = self.graphWidget.plot([], [], pen=pen)

        # sketch point
        self.sketch_point = self.graphWidget.plot([], [], pen=None, symbol='o', symbolBrush='w', symbolSize=5)

        # time reference (seconds)
        self.init_time = time()
        self.prev_time = 0

        # set up timer
        self.timer = QTimer()
        self.timer.setInterval(1/fps)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def update(self):
        t = time() - self.init_time

        # no need to update if no data
        if self.epicycle_chain_x.n == 0:
            return

        self.epicycle_chain_x.update(t)
        self.epicycle_chain_y.update(t)

        # points on circles
        self.points.setData(self.epicycle_chain_x.centers_x + self.epicycle_chain_y.centers_x, 
                            self.epicycle_chain_x.centers_y + self.epicycle_chain_y.centers_y)
        
        # lines connecting circle centers to circle points
        for i, line in enumerate(self.lines_x):
            line.setData([self.epicycle_chain_x.centers_x[i], self.epicycle_chain_x.centers_x[i+1]],
                         [self.epicycle_chain_x.centers_y[i], self.epicycle_chain_x.centers_y[i+1]])
        for i, line in enumerate(self.lines_y):
            line.setData([self.epicycle_chain_y.centers_x[i], self.epicycle_chain_y.centers_x[i+1]],
                         [self.epicycle_chain_y.centers_y[i], self.epicycle_chain_y.centers_y[i+1]])

        # points on circle circumferences
        for i, circle in enumerate(self.circumference_points_x[:-1]):
            circle.setData(self.epicycle_chain_x.circumference_coords_x[i+1], self.epicycle_chain_x.circumference_coords_y[i+1])
        for i, circle in enumerate(self.circumference_points_y[:-1]):
            circle.setData(self.epicycle_chain_y.circumference_coords_x[i+1], self.epicycle_chain_y.circumference_coords_y[i+1])

        x = self.epicycle_chain_y.centers_x[-1]
        y = self.epicycle_chain_x.centers_y[-1]

        # time domain lines
        self.line_x.setData([self.epicycle_chain_x.centers_x[-1], x], [self.epicycle_chain_x.centers_y[-1], self.epicycle_chain_x.centers_y[-1]])
        self.line_y.setData([self.epicycle_chain_y.centers_x[-1], self.epicycle_chain_y.centers_x[-1]], [y, self.epicycle_chain_y.centers_y[-1]])

        # points on sketch
        if self.epicycle_chain_x.n > 0 and len(self.sketch_data_x) < self.period_in_frames:
            self.sketch_data_x.append(x)
            self.sketch_data_y.append(y)
            self.sketch.setData(self.sketch_data_x, self.sketch_data_y)
        
        # sketch point
        self.sketch_point.setData([x], [y])

        # update previous time
        self.prev_time = time() - self.init_time
