# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FigureEditorUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 360)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_left = QtWidgets.QVBoxLayout()
        self.verticalLayout_left.setObjectName("verticalLayout_left")
        self.GraphView = QtWidgets.QWidget(Form)
        self.GraphView.setObjectName("GraphView")
        self.verticalLayout_left.addWidget(self.GraphView)
        self.horizontalLayout_2.addLayout(self.verticalLayout_left)
        self.verticalLayout_right = QtWidgets.QVBoxLayout()
        self.verticalLayout_right.setObjectName("verticalLayout_right")
        self.AxsSelector = QtWidgets.QComboBox(Form)
        self.AxsSelector.setObjectName("AxsSelector")
        self.verticalLayout_right.addWidget(self.AxsSelector)
        self.ElementsSelector = QtWidgets.QComboBox(Form)
        self.ElementsSelector.setObjectName("ElementsSelector")
        self.verticalLayout_right.addWidget(self.ElementsSelector)
        self.Settings = QtWidgets.QWidget(Form)
        self.Settings.setObjectName("Settings")
        self.verticalLayout_right.addWidget(self.Settings)
        self.horizontalLayout_2.addLayout(self.verticalLayout_right)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
