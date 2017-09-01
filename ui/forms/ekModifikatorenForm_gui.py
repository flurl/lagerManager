# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/ekModifikatorenForm.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_EkModifikatorenForm(object):
    def setupUi(self, EkModifikatorenForm):
        EkModifikatorenForm.setObjectName(_fromUtf8("EkModifikatorenForm"))
        EkModifikatorenForm.resize(467, 284)
        self.gridLayout = QtGui.QGridLayout(EkModifikatorenForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_newRecord = QtGui.QPushButton(EkModifikatorenForm)
        self.pushButton_newRecord.setObjectName(_fromUtf8("pushButton_newRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_newRecord)
        self.pushButton_deleteRecord = QtGui.QPushButton(EkModifikatorenForm)
        self.pushButton_deleteRecord.setObjectName(_fromUtf8("pushButton_deleteRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_deleteRecord)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.comboBox_period = QtGui.QComboBox(EkModifikatorenForm)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout_2.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 2)
        self.tableView = QtGui.QTableView(EkModifikatorenForm)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.gridLayout.addWidget(self.tableView, 2, 0, 1, 1)

        self.retranslateUi(EkModifikatorenForm)
        QtCore.QMetaObject.connectSlotsByName(EkModifikatorenForm)

    def retranslateUi(self, EkModifikatorenForm):
        EkModifikatorenForm.setWindowTitle(_translate("EkModifikatorenForm", "Einkaufspreis Modifikatoren", None))
        self.pushButton_newRecord.setText(_translate("EkModifikatorenForm", "&Neu", None))
        self.pushButton_deleteRecord.setText(_translate("EkModifikatorenForm", "&Löschen", None))

