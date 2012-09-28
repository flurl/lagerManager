# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/dokumenteForm.ui'
#
# Created: Thu Sep 27 21:19:42 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DokumenteForm(object):
    def setupUi(self, DokumenteForm):
        DokumenteForm.setObjectName("DokumenteForm")
        DokumenteForm.resize(754, 451)
        self.gridLayout = QtGui.QGridLayout(DokumenteForm)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtGui.QGroupBox(DokumenteForm)
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
        self.tableView_documents = FilterableTableView(self.groupBox)
        self.tableView_documents.setObjectName("tableView_documents")
        self.gridLayout_2.addWidget(self.tableView_documents, 1, 0, 1, 1)
        self.frame = QtGui.QFrame(self.groupBox)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_documentImage = ClickableLabel(self.frame)
        self.label_documentImage.setText("")
        self.label_documentImage.setObjectName("label_documentImage")
        self.gridLayout_3.addWidget(self.label_documentImage, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 2, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(DokumenteForm)
        QtCore.QMetaObject.connectSlotsByName(DokumenteForm)

    def retranslateUi(self, DokumenteForm):
        DokumenteForm.setWindowTitle(QtGui.QApplication.translate("DokumenteForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("DokumenteForm", "Dokumente", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_new.setText(QtGui.QApplication.translate("DokumenteForm", "&Neu", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_edit.setText(QtGui.QApplication.translate("DokumenteForm", "&Bearbeiten", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_delete.setText(QtGui.QApplication.translate("DokumenteForm", "&Löschen", None, QtGui.QApplication.UnicodeUTF8))

from lib.FilterableTableView import FilterableTableView
from lib.ClickableLabel import ClickableLabel
