# from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox


def showdialog(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText(text)
    # msg.setInformativeText("This is additional information")
    msg.setWindowTitle("Error")
    print("error")
    msg.show()
    # msg.setDetailedText("The details are as follows:")
