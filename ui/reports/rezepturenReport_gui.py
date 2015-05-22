# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/rezepturenReport.ui'
#
# Created: Fri May 22 17:16:29 2015
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

class Ui_RezepturenReport(object):
    def setupUi(self, RezepturenReport):
        RezepturenReport.setObjectName(_fromUtf8("RezepturenReport"))
        RezepturenReport.resize(780, 563)
        self.gridLayout = QtGui.QGridLayout(RezepturenReport)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBox_what = QtGui.QComboBox(RezepturenReport)
        self.comboBox_what.setObjectName(_fromUtf8("comboBox_what"))
        self.comboBox_what.addItem(_fromUtf8(""))
        self.comboBox_what.addItem(_fromUtf8(""))
        self.comboBox_what.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox_what)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_export = QtGui.QPushButton(RezepturenReport)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.comboBox_period = QtGui.QComboBox(RezepturenReport)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget = QtGui.QWidget(RezepturenReport)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tableView = FilterableTableView(self.widget)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.horizontalLayout_2.addWidget(self.tableView)
        self.verticalLayout.addWidget(self.widget)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.retranslateUi(RezepturenReport)
        QtCore.QMetaObject.connectSlotsByName(RezepturenReport)

    def retranslateUi(self, RezepturenReport):
        RezepturenReport.setWindowTitle(_translate("RezepturenReport", "Report", None))
        self.comboBox_what.setItemText(0, _translate("RezepturenReport", "Rezepturen", None))
        self.comboBox_what.setItemText(1, _translate("RezepturenReport", "Nicht-Lagerartikel ohne Rezeptur", None))
        self.comboBox_what.setItemText(2, _translate("RezepturenReport", "Rezepturen mit Nicht-Lagerartikel", None))
        self.pushButton_export.setText(_translate("RezepturenReport", "&Exportieren", None))

from lib.FilterableTableView import FilterableTableView
