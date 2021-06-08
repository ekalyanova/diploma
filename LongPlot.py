from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
from numpy import delete, float16, empty, append


class LongPlot(PlotWidget):
    def __init__(self, *args, **kwargs):
        PlotWidget.__init__(self, *args, **kwargs)
        self.init_arrays()

        self.showGrid(x=True, y=True)
        self.data_line = self.plot(
            self.x, self.y, pen=pg.mkPen(width=3, color='#000000'))
        self.controller = None

    def set_upd_timer(self, interval):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(interval)  # in ms
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        # 2 hours * 60 min * 60 sec * 1000sec/interval in ms
        self.N = 2 * 60 * 60 * 1000 / interval

    def update_plot_data(self):
        self.last = self.x[-1]
        if len(self.x) > self.N:
            self.x = self.x[1:]
            self.y = self.y[1:]
        self.x = append(self.x, self.last + 1)
        if self.controller == None:
            self.y = append(self.y, float16(0))
        else:
            self.y = append(self.y, float16(
                self.controller.get_curr_voltage()))
        self.data_line.setData(self.x, self.y)

    def set_controller(self, controller):
        self.controller = controller

    def get_data(self):
        return [self.x, self.y]
    
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def init_arrays(self):
        self.x = empty(1, dtype=float16)
        self.y = empty(1, dtype=float16)

    def clear(self):
        return
        delete(self.x)
        delete(self.y)
        self.init_arrays()
