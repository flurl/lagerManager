# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/buchungskonten2artikelForm.ui'
#
# Created: Mon Jul  8 22:19:33 2013
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

class Ui_Buchungskonten2artikelForm(object):
    def setupUi(self, Buchungskonten2artikelForm):
        Buchungskonten2artikelForm.setObjectName(_fromUtf8("Buchungskonten2artikelForm"))
        Buchungskonten2artikelForm.resize(685, 558)
        self.gridLayout = QtGui.QGridLayout(Buchungskonten2artikelForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_newRecord = QtGui.QPushButton(Buchungskonten2artikelForm)
        self.pushButton_newRecord.setObjectName(_fromUtf8("pushButton_newRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_newRecord)
        self.pushButton_deleteRecord = QtGui.QPushButton(Buchungskonten2artikelForm)
        self.pushButton_deleteRecord.setObjectName(_fromUtf8("pushButton_deleteRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_deleteRecord)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.comboBox_period = QtGui.QComboBox(Buchungskonten2artikelForm)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout_2.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_initPeriod = QtGui.QPushButton(Buchungskonten2artikelForm)
        self.pushButton_initPeriod.setObjectName(_fromUtf8("pushButton_initPeriod"))
        self.horizontalLayout.addWidget(self.pushButton_initPeriod)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 2)
        self.tableView = QtGui.QTableView(Buchungskonten2artikelForm)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.gridLayout.addWidget(self.tableView, 3, 0, 1, 1)

        self.retranslateUi(Buchungskonten2artikelForm)
        QtCore.QMetaObject.connectSlotsByName(Buchungskonten2artikelForm)

    def retranslateUi(self, Buchungskonten2artikelForm):
        Buchungskonten2artikelForm.setWindowTitle(_translate("Buchungskonten2artikelForm", "Buchungskonten Artikeln zuweisen", None))
        self.pushButton_newRecord.setText(_translate("Buchungskonten2artikelForm", "&Neu", None))
        self.pushButton_deleteRecord.setText(_translate("Buchungskonten2artikelForm", "&Löschen", None))
        self.pushButton_initPeriod.setText(_translate("Buchungskonten2artikelForm", "Periode &initialisieren", None))

