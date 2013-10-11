# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/dokumenttypenForm.ui'
#
# Created: Fri Oct 11 12:44:08 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DokumenttypenForm(object):
    def setupUi(self, DokumenttypenForm):
        DokumenttypenForm.setObjectName(_fromUtf8("DokumenttypenForm"))
        DokumenttypenForm.resize(467, 284)
        self.gridLayout = QtGui.QGridLayout(DokumenttypenForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_newRecord = QtGui.QPushButton(DokumenttypenForm)
        self.pushButton_newRecord.setObjectName(_fromUtf8("pushButton_newRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_newRecord)
        self.pushButton_deleteRecord = QtGui.QPushButton(DokumenttypenForm)
        self.pushButton_deleteRecord.setObjectName(_fromUtf8("pushButton_deleteRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_deleteRecord)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.comboBox_period = QtGui.QComboBox(DokumenttypenForm)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout_2.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 2)
        self.tableView_dokumenttypen = QtGui.QTableView(DokumenttypenForm)
        self.tableView_dokumenttypen.setObjectName(_fromUtf8("tableView_dokumenttypen"))
        self.gridLayout.addWidget(self.tableView_dokumenttypen, 2, 0, 1, 1)

        self.retranslateUi(DokumenttypenForm)
        QtCore.QMetaObject.connectSlotsByName(DokumenttypenForm)

    def retranslateUi(self, DokumenttypenForm):
        DokumenttypenForm.setWindowTitle(QtGui.QApplication.translate("DokumenttypenForm", "Dokumentypen", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_newRecord.setText(QtGui.QApplication.translate("DokumenttypenForm", "&Neu", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_deleteRecord.setText(QtGui.QApplication.translate("DokumenttypenForm", "&Löschen", None, QtGui.QApplication.UnicodeUTF8))

