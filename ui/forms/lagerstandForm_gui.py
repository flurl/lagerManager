# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/lagerstandForm.ui'
#
# Created: Thu Jan 17 17:19:52 2013
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LagerstandForm(object):
    def setupUi(self, LagerstandForm):
        LagerstandForm.setObjectName("LagerstandForm")
        LagerstandForm.resize(815, 531)
        self.verticalLayout = QtGui.QVBoxLayout(LagerstandForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_period = QtGui.QComboBox(LagerstandForm)
        self.comboBox_period.setObjectName("comboBox_period")
        self.horizontalLayout.addWidget(self.comboBox_period)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_initPeriod = QtGui.QPushButton(LagerstandForm)
        self.pushButton_initPeriod.setObjectName("pushButton_initPeriod")
        self.horizontalLayout.addWidget(self.pushButton_initPeriod)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView_lagerstand = QtGui.QTableView(LagerstandForm)
        self.tableView_lagerstand.setSortingEnabled(True)
        self.tableView_lagerstand.setObjectName("tableView_lagerstand")
        self.verticalLayout.addWidget(self.tableView_lagerstand)
        self.pushButton_OK = QtGui.QPushButton(LagerstandForm)
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.verticalLayout.addWidget(self.pushButton_OK)

        self.retranslateUi(LagerstandForm)
        QtCore.QMetaObject.connectSlotsByName(LagerstandForm)

    def retranslateUi(self, LagerstandForm):
        LagerstandForm.setWindowTitle(QtGui.QApplication.translate("LagerstandForm", "Lagerstand", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_initPeriod.setText(QtGui.QApplication.translate("LagerstandForm", "&Init Period", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_OK.setText(QtGui.QApplication.translate("LagerstandForm", "&OK", None, QtGui.QApplication.UnicodeUTF8))

