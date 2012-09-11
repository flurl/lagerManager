# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/lagerstandDlg.ui'
#
# Created: Sat Aug 18 23:39:22 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LagerstandDialog(object):
    def setupUi(self, LagerstandDialog):
        LagerstandDialog.setObjectName(_fromUtf8("LagerstandDialog"))
        LagerstandDialog.resize(815, 531)
        self.verticalLayout = QtGui.QVBoxLayout(LagerstandDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBox_period = QtGui.QComboBox(LagerstandDialog)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_initPeriod = QtGui.QPushButton(LagerstandDialog)
        self.pushButton_initPeriod.setObjectName(_fromUtf8("pushButton_initPeriod"))
        self.horizontalLayout.addWidget(self.pushButton_initPeriod)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView_lagerstand = QtGui.QTableView(LagerstandDialog)
        self.tableView_lagerstand.setSortingEnabled(True)
        self.tableView_lagerstand.setObjectName(_fromUtf8("tableView_lagerstand"))
        self.verticalLayout.addWidget(self.tableView_lagerstand)
        self.pushButton_OK = QtGui.QPushButton(LagerstandDialog)
        self.pushButton_OK.setObjectName(_fromUtf8("pushButton_OK"))
        self.verticalLayout.addWidget(self.pushButton_OK)

        self.retranslateUi(LagerstandDialog)
        QtCore.QMetaObject.connectSlotsByName(LagerstandDialog)

    def retranslateUi(self, LagerstandDialog):
        LagerstandDialog.setWindowTitle(QtGui.QApplication.translate("LagerstandDialog", "Lagerstand", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_initPeriod.setText(QtGui.QApplication.translate("LagerstandDialog", "&Init Period", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_OK.setText(QtGui.QApplication.translate("LagerstandDialog", "&OK", None, QtGui.QApplication.UnicodeUTF8))

