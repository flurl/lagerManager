# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/lieferantenDlg.ui'
#
# Created: Wed Aug  1 20:57:39 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LieferantenDialog(object):
    def setupUi(self, LieferantenDialog):
        LieferantenDialog.setObjectName("LieferantenDialog")
        LieferantenDialog.resize(815, 531)
        self.verticalLayout = QtGui.QVBoxLayout(LieferantenDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_newRecord = QtGui.QPushButton(LieferantenDialog)
        self.pushButton_newRecord.setObjectName("pushButton_newRecord")
        self.horizontalLayout.addWidget(self.pushButton_newRecord)
        self.pushButton_deleteRecord = QtGui.QPushButton(LieferantenDialog)
        self.pushButton_deleteRecord.setObjectName("pushButton_deleteRecord")
        self.horizontalLayout.addWidget(self.pushButton_deleteRecord)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView_lieferanten = QtGui.QTableView(LieferantenDialog)
        self.tableView_lieferanten.setObjectName("tableView_lieferanten")
        self.verticalLayout.addWidget(self.tableView_lieferanten)
        self.pushButton_OK = QtGui.QPushButton(LieferantenDialog)
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.verticalLayout.addWidget(self.pushButton_OK)

        self.retranslateUi(LieferantenDialog)
        QtCore.QMetaObject.connectSlotsByName(LieferantenDialog)

    def retranslateUi(self, LieferantenDialog):
        LieferantenDialog.setWindowTitle(QtGui.QApplication.translate("LieferantenDialog", "Lieferanten", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_newRecord.setText(QtGui.QApplication.translate("LieferantenDialog", "&New", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_deleteRecord.setText(QtGui.QApplication.translate("LieferantenDialog", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_OK.setText(QtGui.QApplication.translate("LieferantenDialog", "&OK", None, QtGui.QApplication.UnicodeUTF8))

