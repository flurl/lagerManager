# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/gesamteLieferungenReport.ui'
#
# Created: Thu Jul 30 11:34:15 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_GesamteLieferungenReport(object):
    def setupUi(self, GesamteLieferungenReport):
        GesamteLieferungenReport.setObjectName(_fromUtf8("GesamteLieferungenReport"))
        GesamteLieferungenReport.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(GesamteLieferungenReport)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBox_reportType = QtGui.QComboBox(GesamteLieferungenReport)
        self.comboBox_reportType.setObjectName(_fromUtf8("comboBox_reportType"))
        self.comboBox_reportType.addItem(_fromUtf8(""))
        self.comboBox_reportType.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox_reportType)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_export = QtGui.QPushButton(GesamteLieferungenReport)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.comboBox_period = QtGui.QComboBox(GesamteLieferungenReport)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textView = ReportTextViewWidget(GesamteLieferungenReport)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.verticalLayout.addWidget(self.textView)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.retranslateUi(GesamteLieferungenReport)
        QtCore.QMetaObject.connectSlotsByName(GesamteLieferungenReport)

    def retranslateUi(self, GesamteLieferungenReport):
        GesamteLieferungenReport.setWindowTitle(_translate("GesamteLieferungenReport", "Report", None))
        self.comboBox_reportType.setItemText(0, _translate("GesamteLieferungenReport", "Jährlich", None))
        self.comboBox_reportType.setItemText(1, _translate("GesamteLieferungenReport", "Monatlich", None))
        self.pushButton_export.setText(_translate("GesamteLieferungenReport", "&Exportieren", None))

from reports.reportTextViewWidget import ReportTextViewWidget
