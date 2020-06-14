# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'video_rec.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(196, 140)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 50, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.push_button_selectvideo = QtWidgets.QPushButton(Dialog)
        self.push_button_selectvideo.setGeometry(QtCore.QRect(130, 20, 56, 17))
        self.push_button_selectvideo.setObjectName("push_button_selectvideo")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 80, 56, 17))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(130, 50, 56, 17))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_3.setText(_translate("Dialog", "视频识别"))
        self.push_button_selectvideo.setText(_translate("Dialog", "选择视频"))
        self.pushButton_2.setText(_translate("Dialog", "返回"))
        self.pushButton.setText(_translate("Dialog", "说明"))
