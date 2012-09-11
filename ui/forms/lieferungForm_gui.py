# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/lieferungForm.ui'
#
# Created: Mon Sep 10 20:07:03 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LieferungForm(object):
    def setupUi(self, LieferungForm):
        LieferungForm.setObjectName("LieferungForm")
        LieferungForm.resize(754, 451)
        self.gridLayout = QtGui.QGridLayout(LieferungForm)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtGui.QGroupBox(LieferungForm)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_new = QtGui.QPushButton(self.groupBox)
        self.pushButton_new.setObjectName("pushButton_new")
        self.horizontalLayout_3.addWidget(self.pushButton_new)
        self.pushButton_edit = QtGui.QPushButton(self.groupBox)
        self.pushButton_edit.setObjectName("pushButton_edit")
        self.horizontalLayout_3.addWidget(self.pushButton_edit)
        self.pushButton_delete = QtGui.QPushButton(self.groupBox)
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.horizontalLayout_3.addWidget(self.pushButton_delete)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.comboBox_period = QtGui.QComboBox(self.groupBox)
        self.comboBox_period.setObjectName("comboBox_period")
        self.horizontalLayout_3.addWidget(self.comboBox_period)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.tableView_lieferungen = FilterableTableView(self.groupBox)
        self.tableView_lieferungen.setObjectName("tableView_lieferungen")
        self.gridLayout_2.addWidget(self.tableView_lieferungen, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_2 = QtGui.QGroupBox(LieferungForm)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableView_lieferungenDetails = QtGui.QTableView(self.groupBox_2)
        self.tableView_lieferungenDetails.setObjectName("tableView_lieferungenDetails")
        self.gridLayout_3.addWidget(self.tableView_lieferungenDetails, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(LieferungForm)
        QtCore.QMetaObject.connectSlotsByName(LieferungForm)

    def retranslateUi(self, LieferungForm):
        LieferungForm.setWindowTitle(QtGui.QApplication.translate("LieferungForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("LieferungForm", "Lieferungen", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_new.setText(QtGui.QApplication.translate("LieferungForm", "&Neu", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_edit.setText(QtGui.QApplication.translate("LieferungForm", "&Bearbeiten", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_delete.setText(QtGui.QApplication.translate("LieferungForm", "&Löschen", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("LieferungForm", "Details", None, QtGui.QApplication.UnicodeUTF8))

from lib.FilterableTableView import FilterableTableView
