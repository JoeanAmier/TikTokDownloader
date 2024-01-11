# -*- coding: utf-8 -*-
# @Author : Frica01
# @Time   : 2023-12-28 23:23
# @Name   : main_gui.py


import sys
from ctypes import windll

from PySide6 import QtGui
from PySide6.QtWidgets import QApplication
from gui.controllers.controller_main import ControllerMain

if __name__ == '__main__':
    windll.shell32.SetCurrentProcessExplicitAppUserModelID('nothing')
    app = QApplication([])
    app.setWindowIcon(QtGui.QIcon(r'gui\views\resources\icon.ico'))
    controller = ControllerMain()
    controller.view.show()
    sys.exit(app.exec())
