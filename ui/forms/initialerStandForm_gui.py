# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/initialerStandForm.ui'
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

class Ui_InitialerStandForm(object):
    def setupUi(self, InitialerStandForm):
        InitialerStandForm.setObjectName(_fromUtf8("InitialerStandForm"))
        InitialerStandForm.resize(815, 531)
        self.verticalLayout = QtGui.QVBoxLayout(InitialerStandForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_newRecord = QtGui.QPushButton(InitialerStandForm)
        self.pushButton_newRecord.setObjectName(_fromUtf8("pushButton_newRecord"))
        self.horizontalLayout.addWidget(self.pushButton_newRecord)
        self.pushButton_deleteRecord = QtGui.QPushButton(InitialerStandForm)
        self.pushButton_deleteRecord.setObjectName(_fromUtf8("pushButton_deleteRecord"))
        self.horizontalLayout.addWidget(self.pushButton_deleteRecord)
        self.comboBox_article = QtGui.QComboBox(InitialerStandForm)
        self.comboBox_article.setObjectName(_fromUtf8("comboBox_article"))
        self.horizontalLayout.addWidget(self.comboBox_article)
        self.comboBox_workplace = QtGui.QComboBox(InitialerStandForm)
        self.comboBox_workplace.setObjectName(_fromUtf8("comboBox_workplace"))
        self.horizontalLayout.addWidget(self.comboBox_workplace)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_export = QtGui.QPushButton(InitialerStandForm)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.pushButton_initPeriod = QtGui.QPushButton(InitialerStandForm)
        self.pushButton_initPeriod.setObjectName(_fromUtf8("pushButton_initPeriod"))
        self.horizontalLayout.addWidget(self.pushButton_initPeriod)
        self.comboBox_period = QtGui.QComboBox(InitialerStandForm)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView_lagerstand = QtGui.QTableView(InitialerStandForm)
        self.tableView_lagerstand.setSortingEnabled(True)
        self.tableView_lagerstand.setObjectName(_fromUtf8("tableView_lagerstand"))
        self.verticalLayout.addWidget(self.tableView_lagerstand)

        self.retranslateUi(InitialerStandForm)
        QtCore.QMetaObject.connectSlotsByName(InitialerStandForm)

    def retranslateUi(self, InitialerStandForm):
        InitialerStandForm.setWindowTitle(_translate("InitialerStandForm", "Initialer Stand", None))
        self.pushButton_newRecord.setText(_translate("InitialerStandForm", "&Neu", None))
        self.pushButton_deleteRecord.setText(_translate("InitialerStandForm", "&Löschen", None))
        self.pushButton_export.setText(_translate("InitialerStandForm", "&Export", None))
        self.pushButton_initPeriod.setText(_translate("InitialerStandForm", "&Init Period", None))

