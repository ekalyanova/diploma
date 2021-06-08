from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, setConfigOption
import pyqtgraph as pg
from PyQt5.QtCore import QTimer, QObject
from numpy import delete, float16, empty, append

# 10sec
setConfigOption('background', 'w')
setConfigOption('foreground', '#7f7f7f')


class ShortPlot(PlotWidget):
    def __init__(self, *args, **kwargs):
        # super().__init__()
        PlotWidget.__init__(self, *args, **kwargs)
        self.init_arrays()
        self.showGrid(x=True, y=True)
        self.data_line = self.plot(
            self.x, self.y, pen=pg.mkPen(width=3, color='#000000'))
        self.controller = None

    def set_upd_timer(self, interval):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(interval) 
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        self.N = 10 * 1000 / interval

    def run(self):
        print("shortplot's thread was run")

    def update_plot_data(self):
        if len(self.x) > self.N:
            self.x = self.x[1:]
            self.y = self.y[1:]
        self.x = append(self.x, self.x[-1] + 1)
        if self.controller == None:
            self.y = append(self.y, float16(0))
        else:
            self.y = append(self.y, float16(
                self.controller.get_curr_power()))
        self.data_line.setData(self.x, self.y)

    def set_controller(self, controller):
        self.controller = controller

    def init_arrays(self):
        self.x = empty(1, dtype=float16)
        self.y = empty(1, dtype=float16)

    def clear(self):
        delete(self.x)
        delete(self.y)
        self.init_arrays()
