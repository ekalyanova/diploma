import os
import sys
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from design import Ui_MainWindow
from PyQt5 import QtWidgets
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
# from matplotlib.figure import Figure
import sys
# import matplotlib
# matplotlib.use('Qt5Agg')


# class MainWindow(QtWidgets.QMainWindow):

#     def __init__(self, *args, **kwargs):
#         super(MainWindow, self).__init__(*args, **kwargs)

#         self.graphWidget = pg.PlotWidget()
#         self.setCentralWidget(self.graphWidget)

#         hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#         temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

#         # plot data: x, y values
#         self.graphWidget.plot(hour, temperature)


# class MplCanvas(FigureCanvasQTAgg):

#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # sc = MplCanvas(self, width=5, height=4, dpi=100)
        # sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        # self.setCentralWidget(sc)

        self.setupUi(self)

        # self.short_plot.plot()
        # self.long_plot.plot()
