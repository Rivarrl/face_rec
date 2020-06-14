# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'picture_rec.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(780, 550)
        self.push_button_selectpic = QtWidgets.QPushButton(Dialog)
        self.push_button_selectpic.setGeometry(QtCore.QRect(690, 50, 56, 17))
        self.push_button_selectpic.setObjectName("push_button_selectpic")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 20, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.rec_result = QtWidgets.QLabel(Dialog)
        self.rec_result.setGeometry(QtCore.QRect(20, 50, 641, 481))
        self.rec_result.setText("")
        self.rec_result.setObjectName("rec_result")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(690, 480, 56, 17))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(690, 510, 56, 17))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.push_button_selectpic.setText(_translate("Dialog", "选择图片"))
        self.label_3.setText(_translate("Dialog", "图片识别"))
        self.pushButton.setText(_translate("Dialog", "说明"))
        self.pushButton_2.setText(_translate("Dialog", "退出"))
