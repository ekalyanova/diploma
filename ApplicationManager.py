from pyqtgraph.graphicsItems.DateAxisItem import HOUR_MINUTE_ZOOM_LEVEL
from MainWindow import MainWindow
from arduino import Connection
from Controller import Controller
from CalculatingModule import CalculatingModule
import csv
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
import time
from PyQt5.QtWidgets import QMessageBox

CONNECTION_SPEED = 19200
#in ms:
CONNECTION_UPD_INTERVAL = 1
CONTROLLER_UPD_INTERVAL = 1
SHORTPLOT_UPD_INTERVAL = 1
LONGPLOT_UPD_INTERVAL = 50
HOUR = 60*1000
SAVE_DATA_INTERVAL = HOUR * 2


class ApplicationManager:

    def __init__(self):
        self.gui = MainWindow()

    def run_all_modules(self):
        self.run_arduino_thread()
        self.run_controller_thread()
        self.set_modules()
        # self.set_update_lcds_timer()

# set threads
    def run_arduino_thread(self):
        self.arduino_thread = QtCore.QThread()
        self.connection = Connection()
        self.connection.moveToThread(self.arduino_thread)
        self.connection.connection_error.connect(self.show_error_msg)
        self.connection.set_output_error.connect(self.show_warning_msg)
        self.connection.set_freq_error.connect(self.show_warning_msg)
        self.arduino_thread.started.connect(self.connection.run)
        self.arduino_thread.start()
        self.connection.connect_to_board(self.port, CONNECTION_SPEED)

    def run_controller_thread(self):
        self.controller_thread = QtCore.QThread()
        self.calc_module = CalculatingModule(self.max_power)
        self.controller = Controller(
            self.connection, self.calc_module, self.freq, self.volt)
        self.controller.moveToThread(self.controller_thread)
        # connect signals&slots
        self.controller.upd_statistic.connect(self.update_statistic)
        self.controller.upd_output.connect(self.update_output_lcd)
        self.controller.upd_freq.connect(self.update_freq_lcd)
        self.controller.upd_power.connect(self.update_pwr_lcd)
        self.controller_thread.started.connect(self.controller.run)
        self.controller_thread.start()

# setters

    def set_data(self, port, freq, volt, max_power):
        self.port = port
        self.freq = freq
        self.volt = volt
        self.max_power = max_power

    def set_modules(self):
        self.gui.short_plot.set_controller(self.controller)
        self.gui.long_plot.set_controller(self.controller)
        self.set_buttons()
        self.set_module_timers()

    def set_module_timers(self):  
        self.connection.set_upd_timer(CONNECTION_UPD_INTERVAL)
        self.controller.set_update_arduino_values_timer(
            CONTROLLER_UPD_INTERVAL)
        self.gui.short_plot.set_upd_timer(SHORTPLOT_UPD_INTERVAL)
        self.gui.long_plot.set_upd_timer(LONGPLOT_UPD_INTERVAL)

    def set_buttons(self):
        # freq buttons
        self.gui.set_freq_btn.clicked.connect(self.set_freq)
        self.gui.scan_btn.clicked.connect(self.start_freq_scan)
        # save plots
        self.gui.save_button.clicked.connect(self.save_graph)
        # power buttons
        self.gui.set_pwr_range_btn.clicked.connect(self.set_pwr_range)
        self.gui.change_max_power_btn.clicked.connect(self.change_max_power)

    def set_save_timer(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(SAVE_DATA_INTERVAL)
        self.timer.timeout.connect(self.save_all_data)
        self.timer.start()

# slots
    def update_pwr_lcd(self, pwr):
        self.gui.volt_lcd.display(pwr)

    def update_freq_lcd(self, freq):
        self.gui.freq_lcd.display(freq)

    def update_output_lcd(self, output):
        self.gui.output_volt_lcdNumber.display(output)

    def update_statistic(self):
        self.gui.times_lcdNumber.display(self.controller.get_times())
        self.gui.time_lcdNumber.display(self.controller.get_time())

    def show_error_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(
            "Your board is probably not connected.\nPlease check your connection and restart the app.")
        msg.setWindowTitle("Error")
        msg.exec()

    def show_warning_msg(self, str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(str)
        msg.setWindowTitle("Warning")
        msg.exec()

# teck functions

    def save_graph(self):
        import datetime
        today = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M")
        print(today)
        
        name_file = "power_in_time"
        name_file = name_file + today + ".csv"
        with open(name_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(('time', 'power'))
            rows = zip(self.gui.long_plot.get_x(), self.gui.long_plot.get_y())
            writer.writerows(rows)

        stat_file_name = "statistic_file"
        stat_name = stat_file_name + today + ".txt"  
        stat_file = open(stat_name, "w")
        stat_file.write("number of times:" + str(self.controller.get_times()) + "\n"  )
        stat_file.write("time which the last one was:" + str(self.controller.get_time()) + "\n")

    def save_all_data(self):
        self.save_graph()
        self.gui.long_plot.clear()

# buttons handlers

    def start_freq_scan(self):
        self.controller.start_freq_scan(float(self.gui.start_freq_lineEdit.text(
        )), float(self.gui.final_freq_lineEdit.text()), float(self.gui.step_freq_lineEdit.text()))
        #  start, end, step

    def set_freq(self):
        self.connection.set_freq(int(self.gui.freq_change_line_edit.text()))

    def set_pwr_range(self):
        self.controller.set_pwr_range(float(self.gui.from_pwr_lineEdit.text()),
                                       float(self.gui.to_pwr_lineEdit.text()))

    def change_max_power(self):
        self.controller.change_max_power(
            float(self.gui.max_power_lineEdit.text()))
