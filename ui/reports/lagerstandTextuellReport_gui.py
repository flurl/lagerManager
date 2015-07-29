# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/lagerstandTextuellReport.ui'
#
# Created: Wed Jul 29 17:20:47 2015
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_LagerstandTextuellReport(object):
    def setupUi(self, LagerstandTextuellReport):
        LagerstandTextuellReport.setObjectName(_fromUtf8("LagerstandTextuellReport"))
        LagerstandTextuellReport.resize(989, 500)
        self.gridLayout = QtGui.QGridLayout(LagerstandTextuellReport)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBox_useTillDate = QtGui.QCheckBox(LagerstandTextuellReport)
        self.checkBox_useTillDate.setObjectName(_fromUtf8("checkBox_useTillDate"))
        self.horizontalLayout.addWidget(self.checkBox_useTillDate)
        self.dateEdit_till = QtGui.QDateEdit(LagerstandTextuellReport)
        self.dateEdit_till.setCalendarPopup(True)
        self.dateEdit_till.setObjectName(_fromUtf8("dateEdit_till"))
        self.horizontalLayout.addWidget(self.dateEdit_till)
        self.checkBox_purchasePrice = QtGui.QCheckBox(LagerstandTextuellReport)
        self.checkBox_purchasePrice.setObjectName(_fromUtf8("checkBox_purchasePrice"))
        self.horizontalLayout.addWidget(self.checkBox_purchasePrice)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_export = QtGui.QPushButton(LagerstandTextuellReport)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.comboBox_period = QtGui.QComboBox(LagerstandTextuellReport)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textView = ReportTextViewWidget(LagerstandTextuellReport)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.verticalLayout.addWidget(self.textView)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.retranslateUi(LagerstandTextuellReport)
        QtCore.QMetaObject.connectSlotsByName(LagerstandTextuellReport)

    def retranslateUi(self, LagerstandTextuellReport):
        LagerstandTextuellReport.setWindowTitle(_translate("LagerstandTextuellReport", "Report", None))
        self.checkBox_useTillDate.setText(_translate("LagerstandTextuellReport", "Daten berücksichtigen &nur bis zum ", None))
        self.checkBox_purchasePrice.setText(_translate("LagerstandTextuellReport", "Einkaufs&preis nicht einschränken", None))
        self.pushButton_export.setText(_translate("LagerstandTextuellReport", "&Exportieren", None))

from reports.reportTextViewWidget import ReportTextViewWidget
