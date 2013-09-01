# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/configForm.ui'
#
# Created: Fri Aug 30 23:27:09 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ConfigForm(object):
    def setupUi(self, ConfigForm):
        ConfigForm.setObjectName(_fromUtf8("ConfigForm"))
        ConfigForm.resize(662, 287)
        self.gridLayout = QtGui.QGridLayout(ConfigForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_newRecord = QtGui.QPushButton(ConfigForm)
        self.pushButton_newRecord.setObjectName(_fromUtf8("pushButton_newRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_newRecord)
        self.pushButton_deleteRecord = QtGui.QPushButton(ConfigForm)
        self.pushButton_deleteRecord.setObjectName(_fromUtf8("pushButton_deleteRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_deleteRecord)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.comboBox_period = QtGui.QComboBox(ConfigForm)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout_2.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 2)
        self.tableView = QtGui.QTableView(ConfigForm)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.gridLayout.addWidget(self.tableView, 2, 0, 1, 1)

        self.retranslateUi(ConfigForm)
        QtCore.QMetaObject.connectSlotsByName(ConfigForm)

    def retranslateUi(self, ConfigForm):
        ConfigForm.setWindowTitle(_translate("ConfigForm", "Konfiguration", None))
        self.pushButton_newRecord.setText(_translate("ConfigForm", "&Neu", None))
        self.pushButton_deleteRecord.setText(_translate("ConfigForm", "&Löschen", None))

