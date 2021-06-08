from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, pyqtSignal, QReadWriteLock
import time
from CalculatingModule import CalculatingModule

OFFSET = 0.2  # in V
STAT_UPD_IN_MS = 100
OUT_OF_RANGE_TIMES_TO_CHANGE_VOLTAGE = 3


class Controller(QtCore.QObject):
    upd_statistic = pyqtSignal()
    upd_output = pyqtSignal(float)
    upd_power = pyqtSignal(float)
    upd_freq = pyqtSignal(int)
    
    lock = QReadWriteLock()

    def __init__(self, connection, calc_module, freq, initial_volt):
        super().__init__()
        self.connection = connection
        self.calc_module = calc_module

        self.freq = freq
        self.output_volt = initial_volt

        self.set_initial_values()

        self.time1 = time.time()

    def run(self):
        print("controllers's thread was run")
        self.change_output_voltage()
        self.set_freq(self.freq)

# setters of initialization

    def set_initial_values(self):
        self.curr_voltage = 0
        self.curr_pwr = 0
        self.times = 0
        self.time = 0
        self.max_pwr = 1000
        self.min_pwr = -1
        self.mean_pwr = 5
        self.out_of_range_counter = 0
        self.stat_counter = 0

    def set_update_arduino_values_timer(self, interval):
        self.time1 = time.time()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.update_curr_values)
        self.timer.start()

# setters

    def set_freq(self, freq):
        self.connection.set_freq(freq)
        self.freq = freq
        self.upd_freq.emit(freq)

    def set_pwr_range(self, min_pwr, max_pwr):
        self.max_pwr = max_pwr
        self.min_pwr = min_pwr
        self.mean_pwr = (max_pwr + min_pwr)/2
        print("new mean_pwr", self.mean_pwr)
        self.output_volt = self.calc_module.from_power_to_volt(self.mean_pwr)
        self.change_output_voltage()

    def start_freq_scan(self, start, end, step):
        if start == end or step == 0:
            return
        curr_freq = start
        while curr_freq <= end:
            self.set_freq(curr_freq)
            curr_freq += step

    def change_max_power(self, max_power):
        self.calc_module.change_max_power(max_power)
        self.output_volt = self.calc_module.RF_from_pwr_to_volt(self.mean_pwr)
        self.change_output_voltage()

    def change_output_voltage(self):
        self.connection.set_output(self.output_volt)
        self.upd_output.emit(self.output_volt)

# updates (from timers)

    def update_curr_values(self):              
        self.stat_counter += 1
        if self.stat_counter >= STAT_UPD_IN_MS:
            self.check_pwr()
            self.stat_counter = 0

        self.curr_voltage = self.connection.get_curr_voltage() - OFFSET
        pwr = self.calc_module.from_volt_to_power(self.curr_voltage)
        if pwr < 0:
            return
        self.lock.lockForRead()    
        self.curr_pwr = pwr
        self.lock.unlock()
        self.upd_power.emit(self.curr_pwr)

    def check_pwr(self):
        if self.curr_pwr > self.max_pwr or self.curr_pwr < self.min_pwr and self.curr_pwr > 0:
            self.out_of_range_counter += 1
        if self.out_of_range_counter >= OUT_OF_RANGE_TIMES_TO_CHANGE_VOLTAGE:
            print("OUT OF RANGE")
            self.change_output_voltage()
            self.update_statistic()
            self.out_of_range_counter = 0

    def update_statistic(self):
        self.times += 1

        time2 = time.time()
        self.time = time2 - self.time1
        self.time1 = time2
        self.upd_statistic.emit()

# getters

    def get_curr_voltage(self):
        return self.curr_voltage

    def get_curr_power(self): 
        # lock
        return self.curr_pwr

    def get_curr_freq(self):
        return self.freq

    def get_curr_output(self):
        return self.output_volt

    def get_time(self):
        return self.time

    def get_times(self):
        return self.times
