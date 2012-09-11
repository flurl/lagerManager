# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/connectDlg.ui'
#
# Created: Wed Sep  5 17:48:20 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ConnectDialog(object):
    def setupUi(self, ConnectDialog):
        ConnectDialog.setObjectName("ConnectDialog")
        ConnectDialog.resize(248, 181)
        self.gridLayout = QtGui.QGridLayout(ConnectDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtGui.QLabel(ConnectDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_4 = QtGui.QLabel(ConnectDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_pw = QtGui.QLineEdit(ConnectDialog)
        self.lineEdit_pw.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_pw.setObjectName("lineEdit_pw")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_pw)
        self.comboBox_db = QtGui.QComboBox(ConnectDialog)
        self.comboBox_db.setEditable(True)
        self.comboBox_db.setObjectName("comboBox_db")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBox_db)
        self.label = QtGui.QLabel(ConnectDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_3 = QtGui.QLabel(ConnectDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboBox_host = QtGui.QComboBox(ConnectDialog)
        self.comboBox_host.setEditable(True)
        self.comboBox_host.setObjectName("comboBox_host")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox_host)
        self.comboBox_user = QtGui.QComboBox(ConnectDialog)
        self.comboBox_user.setEditable(True)
        self.comboBox_user.setObjectName("comboBox_user")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBox_user)
        self.verticalLayout.addLayout(self.formLayout)
        self.pushButton_connect = QtGui.QPushButton(ConnectDialog)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.verticalLayout.addWidget(self.pushButton_connect)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(ConnectDialog)
        QtCore.QMetaObject.connectSlotsByName(ConnectDialog)
        ConnectDialog.setTabOrder(self.comboBox_host, self.comboBox_db)
        ConnectDialog.setTabOrder(self.comboBox_db, self.comboBox_user)
        ConnectDialog.setTabOrder(self.comboBox_user, self.lineEdit_pw)
        ConnectDialog.setTabOrder(self.lineEdit_pw, self.pushButton_connect)

    def retranslateUi(self, ConnectDialog):
        ConnectDialog.setWindowTitle(QtGui.QApplication.translate("ConnectDialog", "Verbinden mit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ConnectDialog", "Datenbank", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ConnectDialog", "Paßwort", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ConnectDialog", "Host", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ConnectDialog", "User", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_connect.setText(QtGui.QApplication.translate("ConnectDialog", "&Verbinden", None, QtGui.QApplication.UnicodeUTF8))

