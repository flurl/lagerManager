# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/importForm.ui'
#
# Created: Sun Sep  2 16:47:45 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ImportForm(object):
    def setupUi(self, ImportForm):
        ImportForm.setObjectName(_fromUtf8("ImportForm"))
        ImportForm.resize(197, 201)
        self.gridLayout = QtGui.QGridLayout(ImportForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(ImportForm)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.comboBox_period = QtGui.QComboBox(ImportForm)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox_period)
        self.label_2 = QtGui.QLabel(ImportForm)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_host = QtGui.QLineEdit(ImportForm)
        self.lineEdit_host.setObjectName(_fromUtf8("lineEdit_host"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_host)
        self.label_3 = QtGui.QLabel(ImportForm)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_database = QtGui.QLineEdit(ImportForm)
        self.lineEdit_database.setObjectName(_fromUtf8("lineEdit_database"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_database)
        self.label_4 = QtGui.QLabel(ImportForm)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_user = QtGui.QLineEdit(ImportForm)
        self.lineEdit_user.setObjectName(_fromUtf8("lineEdit_user"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_user)
        self.label_5 = QtGui.QLabel(ImportForm)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_password = QtGui.QLineEdit(ImportForm)
        self.lineEdit_password.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_password.setObjectName(_fromUtf8("lineEdit_password"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_password)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.checkBox_initialImport = QtGui.QCheckBox(ImportForm)
        self.checkBox_initialImport.setObjectName(_fromUtf8("checkBox_initialImport"))
        self.horizontalLayout_3.addWidget(self.checkBox_initialImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_import = QtGui.QPushButton(ImportForm)
        self.pushButton_import.setObjectName(_fromUtf8("pushButton_import"))
        self.horizontalLayout.addWidget(self.pushButton_import)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(ImportForm)
        QtCore.QMetaObject.connectSlotsByName(ImportForm)

    def retranslateUi(self, ImportForm):
        ImportForm.setWindowTitle(QtGui.QApplication.translate("ImportForm", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ImportForm", "Periode", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ImportForm", "Server", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ImportForm", "Datenbank", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ImportForm", "User", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("ImportForm", "Paßwort", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_initialImport.setText(QtGui.QApplication.translate("ImportForm", "Initialer Import", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_import.setText(QtGui.QApplication.translate("ImportForm", "&Importieren", None, QtGui.QApplication.UnicodeUTF8))

