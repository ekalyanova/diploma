from ApplicationManager import ApplicationManager
from PyQt5 import QtWidgets
from InitWindow import InitWindow

if __name__ == "__main__":

    import sys
    qt_app = QtWidgets.QApplication(sys.argv)
    app = ApplicationManager()
    init_app = InitWindow(app)
    init_app.show_gui()
    qt_app.setQuitOnLastWindowClosed(True)
    sys.exit(qt_app.exec_())
