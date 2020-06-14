# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 147)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 471, 111))
        self.groupBox.setObjectName("groupBox")
        self.push_button_selectpath = QtWidgets.QPushButton(self.groupBox)
        self.push_button_selectpath.setGeometry(QtCore.QRect(20, 20, 56, 17))
        self.push_button_selectpath.setObjectName("push_button_selectpath")
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_2.setGeometry(QtCore.QRect(300, 60, 121, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.line_edit_path = QtWidgets.QLineEdit(self.groupBox)
        self.line_edit_path.setGeometry(QtCore.QRect(90, 20, 191, 20))
        self.line_edit_path.setText("")
        self.line_edit_path.setObjectName("line_edit_path")
        self.line_edit_path_2 = QtWidgets.QLineEdit(self.groupBox)
        self.line_edit_path_2.setGeometry(QtCore.QRect(90, 60, 191, 20))
        self.line_edit_path_2.setText("")
        self.line_edit_path_2.setObjectName("line_edit_path_2")
        self.push_button_selectpath_2 = QtWidgets.QPushButton(self.groupBox)
        self.push_button_selectpath_2.setGeometry(QtCore.QRect(20, 60, 56, 17))
        self.push_button_selectpath_2.setObjectName("push_button_selectpath_2")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(300, 20, 121, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(400, 90, 54, 13))
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "模型与数据集选择"))
        self.push_button_selectpath.setText(_translate("Dialog", "选择"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "请选择"))
        self.push_button_selectpath_2.setText(_translate("Dialog", "选择"))
        self.comboBox.setItemText(0, _translate("Dialog", "请选择"))
        self.checkBox.setText(_translate("Dialog", "确认加载"))
