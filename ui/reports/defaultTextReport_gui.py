# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/defaultTextReport.ui'
#
# Created: Mon Aug 20 01:35:53 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

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
        DefaultTextReport.setWindowTitle(QtGui.QApplication.translate("DefaultTextReport", "Report", None, QtGui.QApplication.UnicodeUTF8))

from reports.reportTextViewWidget import ReportTextViewWidget
