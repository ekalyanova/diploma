from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QInputDialog, QApplication, QDialogButtonBox)
from designinit import Ui_Dialog

class InitWindow(QWidget, Ui_Dialog):

    def __init__(self, application_manager):
        super().__init__()
        self.setupUi(self)
        self.application_manager = application_manager
        self.buttonBox.clicked.connect(self.handleButtonClick)

    def reject(self):
        print("reject")

    def accept(self):
        return

    def handleButtonClick(self, button):
        sb = self.buttonBox.standardButton(button)
        if sb == QDialogButtonBox.Ok:
            print('OK Clicked')
            self.close()
            self.port = self.port_lineEdit.text()
            self.freq = int(self.freq_lineEdit.text())
            self.volt = float(self.volt_lineEdit.text())
            self.max_power = float(self.max_power_lineEdit.text())

            self.application_manager.gui.show()
            self.application_manager.set_data(
                self.port, self.freq, self.volt, self.max_power)
            self.application_manager.run_all_modules()

        elif sb == QDialogButtonBox.Cancel:
            print('Cancel Clicked')
            self.close()

    def show_gui(self):
        self.show()
