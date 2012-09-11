# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/lieferanten.ui'
#
# Created: Fri Sep  7 16:30:21 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LieferantenForm(object):
    def setupUi(self, LieferantenForm):
        LieferantenForm.setObjectName("LieferantenForm")
        LieferantenForm.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(LieferantenForm)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_newRecord = QtGui.QPushButton(LieferantenForm)
        self.pushButton_newRecord.setObjectName("pushButton_newRecord")
        self.horizontalLayout_2.addWidget(self.pushButton_newRecord)
        self.pushButton_deleteRecord = QtGui.QPushButton(LieferantenForm)
        self.pushButton_deleteRecord.setObjectName("pushButton_deleteRecord")
        self.horizontalLayout_2.addWidget(self.pushButton_deleteRecord)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 2)
        self.tableView_lieferanten = QtGui.QTableView(LieferantenForm)
        self.tableView_lieferanten.setObjectName("tableView_lieferanten")
        self.gridLayout.addWidget(self.tableView_lieferanten, 2, 0, 1, 1)
        self.pushButton_close = QtGui.QPushButton(LieferantenForm)
        self.pushButton_close.setObjectName("pushButton_close")
        self.gridLayout.addWidget(self.pushButton_close, 3, 0, 1, 1)

        self.retranslateUi(LieferantenForm)
        QtCore.QMetaObject.connectSlotsByName(LieferantenForm)

    def retranslateUi(self, LieferantenForm):
        LieferantenForm.setWindowTitle(QtGui.QApplication.translate("LieferantenForm", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_newRecord.setText(QtGui.QApplication.translate("LieferantenForm", "&Neu", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_deleteRecord.setText(QtGui.QApplication.translate("LieferantenForm", "&Löschen", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_close.setText(QtGui.QApplication.translate("LieferantenForm", "&Schließen", None, QtGui.QApplication.UnicodeUTF8))

