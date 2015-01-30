# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/defaultTableReport.ui'
#
# Created: Tue Nov 11 17:34:31 2014
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

class Ui_DefaultTableReport(object):
    def setupUi(self, DefaultTableReport):
        DefaultTableReport.setObjectName(_fromUtf8("DefaultTableReport"))
        DefaultTableReport.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(DefaultTableReport)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_export = QtGui.QPushButton(DefaultTableReport)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.comboBox_period = QtGui.QComboBox(DefaultTableReport)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget = QtGui.QWidget(DefaultTableReport)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout.addWidget(self.widget)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.retranslateUi(DefaultTableReport)
        QtCore.QMetaObject.connectSlotsByName(DefaultTableReport)

    def retranslateUi(self, DefaultTableReport):
        DefaultTableReport.setWindowTitle(_translate("DefaultTableReport", "Report", None))
        self.pushButton_export.setText(_translate("DefaultTableReport", "&Exportieren", None))

