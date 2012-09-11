# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/defaultGraphicsReport.ui'
#
# Created: Mon Aug 20 01:01:56 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DefaultGraphicsReport(object):
    def setupUi(self, DefaultGraphicsReport):
        DefaultGraphicsReport.setObjectName(_fromUtf8("DefaultGraphicsReport"))
        DefaultGraphicsReport.resize(809, 709)
        self.gridLayout = QtGui.QGridLayout(DefaultGraphicsReport)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.comboBox_period = QtGui.QComboBox(DefaultGraphicsReport)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.graphicsView = ReportGraphicsViewWidget(DefaultGraphicsReport)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout.addWidget(self.graphicsView)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.retranslateUi(DefaultGraphicsReport)
        QtCore.QMetaObject.connectSlotsByName(DefaultGraphicsReport)

    def retranslateUi(self, DefaultGraphicsReport):
        DefaultGraphicsReport.setWindowTitle(QtGui.QApplication.translate("DefaultGraphicsReport", "Report", None, QtGui.QApplication.UnicodeUTF8))

from reports.reportGraphicsViewWidget import ReportGraphicsViewWidget
