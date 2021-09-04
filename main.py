#!/usr/bin/env python3
import sys

from PyQt5 import QtWidgets
from gpiozero import DigitalOutputDevice

from ui.test import Ui_MainWindow


class MainWindow(Ui_MainWindow):
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()
        self.setupUi(self.main_window)

        self.pushButton.clicked.connect(self.button1)
        self.pushButton_2.clicked.connect(self.button2)
        self.pushButton_3.clicked.connect(self.button3)
        self.pushButton_4.clicked.connect(self.button4)
        self.pushButton_5.clicked.connect(self.button5)
        self.pushButton_6.clicked.connect(self.button6)

    def show(self):
        self.main_window.show()
        self.app.exec_()

    def button1(self):
        out1.toggle()
        self.label.setText('On' if out1.is_active else 'Off')

    def button2(self):
        out2.toggle()
        self.label_2.setText('On' if out2.is_active else 'Off')

    def button3(self):
        out3.toggle()
        self.label_3.setText('On' if out3.is_active else 'Off')

    def button4(self):
        out4.toggle()
        self.label_4.setText('On' if out4.is_active else 'Off')

    def button5(self):
        out5.toggle()
        self.label_5.setText('On' if out5.is_active else 'Off')

    def button6(self):
        out6.toggle()
        self.label_6.setText('On' if out6.is_active else 'Off')


if __name__ == '__main__':
    out5 = DigitalOutputDevice(12)
    out6 = DigitalOutputDevice(6)
    out1 = DigitalOutputDevice(5)
    out2 = DigitalOutputDevice(13)
    out3 = DigitalOutputDevice(17)
    out4 = DigitalOutputDevice(18)

    main_window = MainWindow()
    main_window.show()
