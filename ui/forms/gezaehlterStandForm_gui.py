# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/gezaehlterStandForm.ui'
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

class Ui_GezaehlterStandForm(object):
    def setupUi(self, GezaehlterStandForm):
        GezaehlterStandForm.setObjectName(_fromUtf8("GezaehlterStandForm"))
        GezaehlterStandForm.resize(815, 531)
        self.verticalLayout = QtGui.QVBoxLayout(GezaehlterStandForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_newRecord = QtGui.QPushButton(GezaehlterStandForm)
        self.pushButton_newRecord.setObjectName(_fromUtf8("pushButton_newRecord"))
        self.horizontalLayout.addWidget(self.pushButton_newRecord)
        self.pushButton_deleteRecord = QtGui.QPushButton(GezaehlterStandForm)
        self.pushButton_deleteRecord.setObjectName(_fromUtf8("pushButton_deleteRecord"))
        self.horizontalLayout.addWidget(self.pushButton_deleteRecord)
        self.comboBox_article = QtGui.QComboBox(GezaehlterStandForm)
        self.comboBox_article.setObjectName(_fromUtf8("comboBox_article"))
        self.horizontalLayout.addWidget(self.comboBox_article)
        self.comboBox_date = QtGui.QComboBox(GezaehlterStandForm)
        self.comboBox_date.setObjectName(_fromUtf8("comboBox_date"))
        self.horizontalLayout.addWidget(self.comboBox_date)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_export = QtGui.QPushButton(GezaehlterStandForm)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.dateEdit_initDate = QtGui.QDateEdit(GezaehlterStandForm)
        self.dateEdit_initDate.setCalendarPopup(True)
        self.dateEdit_initDate.setObjectName(_fromUtf8("dateEdit_initDate"))
        self.horizontalLayout.addWidget(self.dateEdit_initDate)
        self.pushButton_initPeriod = QtGui.QPushButton(GezaehlterStandForm)
        self.pushButton_initPeriod.setObjectName(_fromUtf8("pushButton_initPeriod"))
        self.horizontalLayout.addWidget(self.pushButton_initPeriod)
        self.comboBox_period = QtGui.QComboBox(GezaehlterStandForm)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView_lagerstand = QtGui.QTableView(GezaehlterStandForm)
        self.tableView_lagerstand.setSortingEnabled(True)
        self.tableView_lagerstand.setObjectName(_fromUtf8("tableView_lagerstand"))
        self.verticalLayout.addWidget(self.tableView_lagerstand)

        self.retranslateUi(GezaehlterStandForm)
        QtCore.QMetaObject.connectSlotsByName(GezaehlterStandForm)

    def retranslateUi(self, GezaehlterStandForm):
        GezaehlterStandForm.setWindowTitle(_translate("GezaehlterStandForm", "Gezählter Stand", None))
        self.pushButton_newRecord.setText(_translate("GezaehlterStandForm", "&Neu", None))
        self.pushButton_deleteRecord.setText(_translate("GezaehlterStandForm", "&Löschen", None))
        self.pushButton_export.setText(_translate("GezaehlterStandForm", "&Export", None))
        self.pushButton_initPeriod.setText(_translate("GezaehlterStandForm", "&Init Datum", None))

