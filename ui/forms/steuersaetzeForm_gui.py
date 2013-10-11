# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/steuersaetzeForm.ui'
#
# Created: Fri Oct 11 12:47:49 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SteuersaetzeForm(object):
    def setupUi(self, SteuersaetzeForm):
        SteuersaetzeForm.setObjectName(_fromUtf8("SteuersaetzeForm"))
        SteuersaetzeForm.resize(467, 284)
        self.gridLayout = QtGui.QGridLayout(SteuersaetzeForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_newRecord = QtGui.QPushButton(SteuersaetzeForm)
        self.pushButton_newRecord.setObjectName(_fromUtf8("pushButton_newRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_newRecord)
        self.pushButton_deleteRecord = QtGui.QPushButton(SteuersaetzeForm)
        self.pushButton_deleteRecord.setObjectName(_fromUtf8("pushButton_deleteRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_deleteRecord)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.comboBox_period = QtGui.QComboBox(SteuersaetzeForm)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout_2.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 2)
        self.tableView_steuersaetze = QtGui.QTableView(SteuersaetzeForm)
        self.tableView_steuersaetze.setObjectName(_fromUtf8("tableView_steuersaetze"))
        self.gridLayout.addWidget(self.tableView_steuersaetze, 2, 0, 1, 1)

        self.retranslateUi(SteuersaetzeForm)
        QtCore.QMetaObject.connectSlotsByName(SteuersaetzeForm)

    def retranslateUi(self, SteuersaetzeForm):
        SteuersaetzeForm.setWindowTitle(QtGui.QApplication.translate("SteuersaetzeForm", "Steuersätze", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_newRecord.setText(QtGui.QApplication.translate("SteuersaetzeForm", "&Neu", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_deleteRecord.setText(QtGui.QApplication.translate("SteuersaetzeForm", "&Löschen", None, QtGui.QApplication.UnicodeUTF8))

