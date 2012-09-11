# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/periodenDlg.ui'
#
# Created: Wed Aug  1 21:57:26 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PeriodenDialog(object):
    def setupUi(self, PeriodenDialog):
        PeriodenDialog.setObjectName("PeriodenDialog")
        PeriodenDialog.resize(815, 531)
        self.verticalLayout = QtGui.QVBoxLayout(PeriodenDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_newRecord = QtGui.QPushButton(PeriodenDialog)
        self.pushButton_newRecord.setObjectName("pushButton_newRecord")
        self.horizontalLayout.addWidget(self.pushButton_newRecord)
        self.pushButton_deleteRecord = QtGui.QPushButton(PeriodenDialog)
        self.pushButton_deleteRecord.setObjectName("pushButton_deleteRecord")
        self.horizontalLayout.addWidget(self.pushButton_deleteRecord)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView_perioden = QtGui.QTableView(PeriodenDialog)
        self.tableView_perioden.setObjectName("tableView_perioden")
        self.verticalLayout.addWidget(self.tableView_perioden)
        self.pushButton_OK = QtGui.QPushButton(PeriodenDialog)
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.verticalLayout.addWidget(self.pushButton_OK)

        self.retranslateUi(PeriodenDialog)
        QtCore.QMetaObject.connectSlotsByName(PeriodenDialog)

    def retranslateUi(self, PeriodenDialog):
        PeriodenDialog.setWindowTitle(QtGui.QApplication.translate("PeriodenDialog", "Perioden", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_newRecord.setText(QtGui.QApplication.translate("PeriodenDialog", "&New", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_deleteRecord.setText(QtGui.QApplication.translate("PeriodenDialog", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_OK.setText(QtGui.QApplication.translate("PeriodenDialog", "&OK", None, QtGui.QApplication.UnicodeUTF8))

