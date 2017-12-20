# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 12:31:56 2017

@author: Rebecca Cui
"""

import sys
import prototype
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = prototype.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
