# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/lieferungenDlg.ui'
#
# Created: Thu Aug  2 15:17:48 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LieferungenDialog(object):
    def setupUi(self, LieferungenDialog):
        LieferungenDialog.setObjectName("LieferungenDialog")
        LieferungenDialog.resize(812, 516)
        self.verticalLayout_2 = QtGui.QVBoxLayout(LieferungenDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtGui.QGroupBox(LieferungenDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_newLieferung = QtGui.QPushButton(self.groupBox)
        self.pushButton_newLieferung.setObjectName("pushButton_newLieferung")
        self.horizontalLayout.addWidget(self.pushButton_newLieferung)
        self.pushButton_deleteLieferung = QtGui.QPushButton(self.groupBox)
        self.pushButton_deleteLieferung.setObjectName("pushButton_deleteLieferung")
        self.horizontalLayout.addWidget(self.pushButton_deleteLieferung)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.tableView_lieferungen = QtGui.QTableView(self.groupBox)
        self.tableView_lieferungen.setObjectName("tableView_lieferungen")
        self.verticalLayout_3.addWidget(self.tableView_lieferungen)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(LieferungenDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_newDetail = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_newDetail.setObjectName("pushButton_newDetail")
        self.horizontalLayout_2.addWidget(self.pushButton_newDetail)
        self.pushButton_deleteDetail = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_deleteDetail.setObjectName("pushButton_deleteDetail")
        self.horizontalLayout_2.addWidget(self.pushButton_deleteDetail)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableView_lieferungenDetails = QtGui.QTableView(self.groupBox_2)
        self.tableView_lieferungenDetails.setObjectName("tableView_lieferungenDetails")
        self.verticalLayout.addWidget(self.tableView_lieferungenDetails)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.pushButton_OK = QtGui.QPushButton(LieferungenDialog)
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.verticalLayout_2.addWidget(self.pushButton_OK)

        self.retranslateUi(LieferungenDialog)
        QtCore.QMetaObject.connectSlotsByName(LieferungenDialog)

    def retranslateUi(self, LieferungenDialog):
        LieferungenDialog.setWindowTitle(QtGui.QApplication.translate("LieferungenDialog", "Lieferungen", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("LieferungenDialog", "Lieferungen", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_newLieferung.setText(QtGui.QApplication.translate("LieferungenDialog", "&Hinzufügen", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_deleteLieferung.setText(QtGui.QApplication.translate("LieferungenDialog", "&Löschen", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("LieferungenDialog", "Lieferungen Details", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_newDetail.setText(QtGui.QApplication.translate("LieferungenDialog", "&Hinzufügen", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_deleteDetail.setText(QtGui.QApplication.translate("LieferungenDialog", "&Löschen", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_OK.setText(QtGui.QApplication.translate("LieferungenDialog", "&OK", None, QtGui.QApplication.UnicodeUTF8))

