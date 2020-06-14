# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(330, 266)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.push_button_about = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_about.setGeometry(QtCore.QRect(230, 30, 56, 17))
        self.push_button_about.setObjectName("push_button_about")
        self.push_button_exit = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_exit.setGeometry(QtCore.QRect(230, 50, 56, 17))
        self.push_button_exit.setObjectName("push_button_exit")
        self.push_button_camera = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_camera.setGeometry(QtCore.QRect(90, 160, 56, 17))
        self.push_button_camera.setObjectName("push_button_camera")
        self.push_button_picture = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_picture.setGeometry(QtCore.QRect(90, 130, 56, 17))
        self.push_button_picture.setObjectName("push_button_picture")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 220, 81, 16))
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(100, 80, 71, 21))
        self.label_4.setObjectName("label_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 240, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 30, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(22)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.push_button_video = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_video.setGeometry(QtCore.QRect(90, 190, 56, 17))
        self.push_button_video.setObjectName("push_button_video")
        self.push_button_settings = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_settings.setGeometry(QtCore.QRect(90, 220, 56, 17))
        self.push_button_settings.setObjectName("push_button_settings")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.push_button_about.setText(_translate("MainWindow", "关于"))
        self.push_button_exit.setText(_translate("MainWindow", "退出"))
        self.push_button_camera.setText(_translate("MainWindow", "摄像头识别"))
        self.push_button_picture.setText(_translate("MainWindow", "图片识别"))
        self.label.setText(_translate("MainWindow", "@ Made By Rivarrl"))
        self.label_4.setText(_translate("MainWindow", "欢迎使用！"))
        self.label_2.setText(_translate("MainWindow", "2020/3/24"))
        self.label_3.setText(_translate("MainWindow", "人脸识别程序"))
        self.push_button_video.setText(_translate("MainWindow", "视频识别"))
        self.push_button_settings.setText(_translate("MainWindow", "设置"))
