# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
import sys

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        w = MainWindow()
        sys.exit(app.exec_())
    except:
        print(1)


