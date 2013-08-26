# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/defaultTextReport.ui'
#
# Created: Mon Aug 26 14:55:31 2013
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

class Ui_DefaultTextReport(object):
    def setupUi(self, DefaultTextReport):
        DefaultTextReport.setObjectName(_fromUtf8("DefaultTextReport"))
        DefaultTextReport.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(DefaultTextReport)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_export = QtGui.QPushButton(DefaultTextReport)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.comboBox_period = QtGui.QComboBox(DefaultTextReport)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textView = ReportTextViewWidget(DefaultTextReport)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.verticalLayout.addWidget(self.textView)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.retranslateUi(DefaultTextReport)
        QtCore.QMetaObject.connectSlotsByName(DefaultTextReport)

    def retranslateUi(self, DefaultTextReport):
        DefaultTextReport.setWindowTitle(_translate("DefaultTextReport", "Report", None))
        self.pushButton_export.setText(_translate("DefaultTextReport", "&Exportieren", None))

from reports.reportTextViewWidget import ReportTextViewWidget
