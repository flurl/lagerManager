# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/reportTextView.ui'
#
# Created: Mon Aug 20 00:45:52 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ReportTextView(object):
    def setupUi(self, ReportTextView):
        ReportTextView.setObjectName(_fromUtf8("ReportTextView"))
        ReportTextView.resize(531, 459)
        self.gridLayout = QtGui.QGridLayout(ReportTextView)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = QtGui.QTextEdit(ReportTextView)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.textEdit)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(ReportTextView)
        QtCore.QMetaObject.connectSlotsByName(ReportTextView)

    def retranslateUi(self, ReportTextView):
        ReportTextView.setWindowTitle(QtGui.QApplication.translate("ReportTextView", "Form", None, QtGui.QApplication.UnicodeUTF8))

