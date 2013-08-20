# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/buchungskontenForm.ui'
#
# Created: Tue Aug 20 17:35:39 2013
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

class Ui_BuchungskontenForm(object):
    def setupUi(self, BuchungskontenForm):
        BuchungskontenForm.setObjectName(_fromUtf8("BuchungskontenForm"))
        BuchungskontenForm.resize(467, 284)
        self.gridLayout = QtGui.QGridLayout(BuchungskontenForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_newRecord = QtGui.QPushButton(BuchungskontenForm)
        self.pushButton_newRecord.setObjectName(_fromUtf8("pushButton_newRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_newRecord)
        self.pushButton_deleteRecord = QtGui.QPushButton(BuchungskontenForm)
        self.pushButton_deleteRecord.setObjectName(_fromUtf8("pushButton_deleteRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_deleteRecord)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.comboBox_period = QtGui.QComboBox(BuchungskontenForm)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout_2.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 2)
        self.tableView = QtGui.QTableView(BuchungskontenForm)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.gridLayout.addWidget(self.tableView, 4, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_openBuchungskonten2ArtikelForm = QtGui.QPushButton(BuchungskontenForm)
        self.pushButton_openBuchungskonten2ArtikelForm.setObjectName(_fromUtf8("pushButton_openBuchungskonten2ArtikelForm"))
        self.horizontalLayout.addWidget(self.pushButton_openBuchungskonten2ArtikelForm)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.retranslateUi(BuchungskontenForm)
        QtCore.QMetaObject.connectSlotsByName(BuchungskontenForm)

    def retranslateUi(self, BuchungskontenForm):
        BuchungskontenForm.setWindowTitle(_translate("BuchungskontenForm", "Buchungskonten", None))
        self.pushButton_newRecord.setText(_translate("BuchungskontenForm", "&Neu", None))
        self.pushButton_deleteRecord.setText(_translate("BuchungskontenForm", "&Löschen", None))
        self.pushButton_openBuchungskonten2ArtikelForm.setText(_translate("BuchungskontenForm", "&Artikel zuweisen", None))

