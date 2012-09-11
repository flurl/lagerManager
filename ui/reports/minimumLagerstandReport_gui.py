# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/minimumLagerstandReport.ui'
#
# Created: Sat Aug 18 04:18:07 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MinimumLagerstand(object):
    def setupUi(self, MinimumLagerstand):
        MinimumLagerstand.setObjectName(_fromUtf8("MinimumLagerstand"))
        MinimumLagerstand.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(MinimumLagerstand)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textView = ReportTextViewWidget(MinimumLagerstand)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.verticalLayout.addWidget(self.textView)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(MinimumLagerstand)
        QtCore.QMetaObject.connectSlotsByName(MinimumLagerstand)

    def retranslateUi(self, MinimumLagerstand):
        MinimumLagerstand.setWindowTitle(QtGui.QApplication.translate("MinimumLagerstand", "Minimum Erreicht", None, QtGui.QApplication.UnicodeUTF8))

from reports.reportTextViewWidget import ReportTextViewWidget
