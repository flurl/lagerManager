# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/lib/FilterableTableView.ui'
#
# Created: Sun Sep  2 15:39:00 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FilterableTableView(object):
    def setupUi(self, FilterableTableView):
        FilterableTableView.setObjectName(_fromUtf8("FilterableTableView"))
        FilterableTableView.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(FilterableTableView)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.layout_filters = QtGui.QHBoxLayout()
        self.layout_filters.setObjectName(_fromUtf8("layout_filters"))
        self.verticalLayout.addLayout(self.layout_filters)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.tableView = QtGui.QTableView(FilterableTableView)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)

        self.retranslateUi(FilterableTableView)
        QtCore.QMetaObject.connectSlotsByName(FilterableTableView)

    def retranslateUi(self, FilterableTableView):
        FilterableTableView.setWindowTitle(QtGui.QApplication.translate("FilterableTableView", "Form", None, QtGui.QApplication.UnicodeUTF8))

