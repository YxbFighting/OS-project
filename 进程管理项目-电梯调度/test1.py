# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from thread_construct import Elevator, GroupOfElevator
import sys

e1 = GroupOfElevator(())

class Ui_MainWindow(object):
    def __init__(self):
        self.number = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(80, 160, 111, 71))
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 190, 201, 61))
        self.pushButton_2.setObjectName("pushButton_2")

        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(60, 310, 181, 71))
        self.lcdNumber.setObjectName("lcdNumber")

        self.lcdNumber.setStyleSheet("border: 2px solid silver; color: white; background: black;")
        self.TimerOfLcd = QTimer()  # 定时器
        self.TimerOfLcd.timeout.connect(self.refresh)
        self.TimerOfLcd.start(10)  # 每0.001s 更新一次

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_1.clicked.connect(lambda: self.output1(100))
        self.pushButton_2.clicked.connect(self.output2)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_1.setText(_translate("MainWindow", "PushButton1"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton2"))

    def refresh(self):
        self.lcdNumber.display(e1.e2.floor)

    def output1(self,a):
        print(a)
        e1.ele_task[3] = [4]
        self.pushButton_1.setStyleSheet("background-color: rgb(255, 150, 3);")
        return 1

    def output2(self):
        e1.ele_task[1] = [5]
        return 2


def multithreading():
    # 创建线程

    e1.setDaemon(True)
    e1.start()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

    e1.join()


if __name__ == "__main__":
    multithreading()


