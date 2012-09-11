# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/lieferungDetailForm.ui'
#
# Created: Mon Sep 10 20:04:54 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LieferungDetailForm(object):
    def setupUi(self, LieferungDetailForm):
        LieferungDetailForm.setObjectName("LieferungDetailForm")
        LieferungDetailForm.resize(673, 383)
        self.gridLayout = QtGui.QGridLayout(LieferungDetailForm)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtGui.QGroupBox(LieferungDetailForm)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_id = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_id.setReadOnly(True)
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_id)
        self.comboBox_lieferant = QtGui.QComboBox(self.groupBox)
        self.comboBox_lieferant.setObjectName("comboBox_lieferant")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBox_lieferant)
        self.dateEdit_datum = QtGui.QDateEdit(self.groupBox)
        self.dateEdit_datum.setCalendarPopup(True)
        self.dateEdit_datum.setObjectName("dateEdit_datum")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.dateEdit_datum)
        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(LieferungDetailForm)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(LieferungDetailForm)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_newDetail = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_newDetail.setObjectName("pushButton_newDetail")
        self.horizontalLayout.addWidget(self.pushButton_newDetail)
        self.pushButton_deleteDetail = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_deleteDetail.setObjectName("pushButton_deleteDetail")
        self.horizontalLayout.addWidget(self.pushButton_deleteDetail)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView_details = QtGui.QTableView(self.groupBox_2)
        self.tableView_details.setObjectName("tableView_details")
        self.verticalLayout.addWidget(self.tableView_details)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.retranslateUi(LieferungDetailForm)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), LieferungDetailForm.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), LieferungDetailForm.reject)
        QtCore.QMetaObject.connectSlotsByName(LieferungDetailForm)

    def retranslateUi(self, LieferungDetailForm):
        LieferungDetailForm.setWindowTitle(QtGui.QApplication.translate("LieferungDetailForm", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("LieferungDetailForm", "Lieferung", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LieferungDetailForm", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LieferungDetailForm", "Lieferant", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("LieferungDetailForm", "Datum", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("LieferungDetailForm", "Details", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_newDetail.setText(QtGui.QApplication.translate("LieferungDetailForm", "&Hinzufügen", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_deleteDetail.setText(QtGui.QApplication.translate("LieferungDetailForm", "&Löschen", None, QtGui.QApplication.UnicodeUTF8))

