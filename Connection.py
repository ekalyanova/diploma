import serial
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, pyqtSignal,  QReadWriteLock
# from random import randint
import time


def calc_freq(freq):
    k10 = int(float(freq) * (10 ** 6) * (2 ** 31) / (10 ** 9))
    print("Контрольное число: ", k10)

    bk10 = bin(k10)
    bk2 = str(bk10)
    # print(bk10)
    if len(bk2) == 31:
        bs = str(bk10)[2:13] + '000000000000000000'
        bss = bs[0:11] + 'h'
        # print(bs.encode('utf-8'))
    elif len(bk2) == 30:
        bs = '0' + str(bk10)[2:12] + '000000000000000000'
        bss = bs[0:11] + 'h'
        # print(bs.encode('utf-8'))
    elif len(bk2) == 29:
        bs = '00' + str(bk10)[2:11] + '000000000000000000'
        bss = bs[0:11] + 'h'
        # print(bs.encode('utf-8'))
    else:
        print("Неподходящая длина бинарной последовательности")
    ds = int(bs, 2)
    # print("bs=, ds =", bs, ds)
    f = ds * (10 ** 9) / ((10 ** 6) * (2 ** 31))
    # print(f)
    # bss = bytes(bss, 'utf-8')
    # ibss = int.from_bytes(bss, "big")
    # print("bss", bss)
    ibss = []
    for i in bss[:11]:
        ibss.append(int(i))
    ibss.append(0)
    print('ibss = ', ibss)
    return ibss


class Connection(QtCore.QObject):
    connection_error = pyqtSignal()
    set_output_error = pyqtSignal(str)
    set_freq_error = pyqtSignal(str)
    lock = QReadWriteLock()

    def __init__(self):
        super().__init__()
        self.voltage = 0

        freq_key = 1
        self.freq_key = freq_key.to_bytes(1, 'big')
        volt_key = 3
        self.volt_key = volt_key.to_bytes(1, 'big')

        self.flush_counter = 0

    def connect_to_board(self, port, speed):
        try:          
            self.ser = serial.Serial(port, speed)
        except serial.serialutil.SerialException:
            self.connection_error.emit()

    def set_upd_timer(self, interval):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.get_numb_from_arduino)
        self.timer.start()

    def run(self):
        print("arduino's thread was run")

    def get_numb_from_arduino(self):
        try:
            adc_volt = self.ser.readline()
        except AttributeError:
            # print("cannot read")
            return
        try:
            iadc_volt = int(adc_volt)
        except ValueError:
            iadc_volt = int.from_bytes(adc_volt, "big")
            # print("cannot convert", adc_volt, iadc_volt)
            return
        if iadc_volt > 1024:
            print("more than 1024")
            return
        self.lock.lockForRead()
        self.voltage = self.from_adc_to_volt(iadc_volt)
        self.lock.unlock()
        self.flush_counter += 1
        if self.flush_counter == 50:
            self.flush_input_values()
            self.flush_counter = 0
        # print("VOLTAGE", self.voltage)

    def get_curr_voltage(self):
        return self.voltage

    def get_curr_freq(self):
        return self.freq

    def set_output(self, volt):
        adc_volt = self.from_volt_to_adc(volt)
        byte_volt = adc_volt.to_bytes(1, 'big')
        try:
            self.ser.write(self.volt_key)
            time.sleep(0.05)
            self.ser.write(byte_volt)
        except AttributeError:
            self.set_output_error.emit("Output voltage wasn't set")
            return
        # time.sleep(0.05)

    def flush_input_values(self):
        try:
            self.ser.flushInput()
        except AttributeError:
            print("i couldn't flush")
            return

    def from_volt_to_adc(self, volt):
        return round(volt * 1024 / 5)

    def from_adc_to_volt(self, adc_volt):
        return adc_volt * 5 / 1024

    def set_freq(self, freq):
        self.freq = freq
        converted_freq = calc_freq(freq)
        print(converted_freq)
        try:
            self.ser.write(self.freq_key)
            time.sleep(0.05)
            self.ser.write(converted_freq)
        except AttributeError:
            self.set_freq_error.emit("Frequency voltage wasn't set")
            return

    def __del__(self):
        print('bye')
        self.ser.close()
