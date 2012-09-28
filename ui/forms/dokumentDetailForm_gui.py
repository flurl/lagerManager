# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/dokumentDetailForm.ui'
#
# Created: Fri Sep 28 15:01:28 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DokumentDetailForm(object):
    def setupUi(self, DokumentDetailForm):
        DokumentDetailForm.setObjectName("DokumentDetailForm")
        DokumentDetailForm.resize(450, 255)
        self.gridLayout = QtGui.QGridLayout(DokumentDetailForm)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtGui.QGroupBox(DokumentDetailForm)
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
        self.comboBox_typ = QtGui.QComboBox(self.groupBox)
        self.comboBox_typ.setObjectName("comboBox_typ")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBox_typ)
        self.dateEdit_datum = QtGui.QDateEdit(self.groupBox)
        self.dateEdit_datum.setCalendarPopup(True)
        self.dateEdit_datum.setObjectName("dateEdit_datum")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.dateEdit_datum)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_fileChooser = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_fileChooser.sizePolicy().hasHeightForWidth())
        self.pushButton_fileChooser.setSizePolicy(sizePolicy)
        self.pushButton_fileChooser.setObjectName("pushButton_fileChooser")
        self.horizontalLayout_2.addWidget(self.pushButton_fileChooser)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)
        self.label_documentImage = ClickableLabel(self.groupBox)
        self.label_documentImage.setText("")
        self.label_documentImage.setObjectName("label_documentImage")
        self.gridLayout_2.addWidget(self.label_documentImage, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DokumentDetailForm)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(DokumentDetailForm)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DokumentDetailForm.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DokumentDetailForm.reject)
        QtCore.QMetaObject.connectSlotsByName(DokumentDetailForm)

    def retranslateUi(self, DokumentDetailForm):
        DokumentDetailForm.setWindowTitle(QtGui.QApplication.translate("DokumentDetailForm", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("DokumentDetailForm", "Lieferung", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DokumentDetailForm", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DokumentDetailForm", "Typ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DokumentDetailForm", "Datum", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("DokumentDetailForm", "Datei", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_fileChooser.setText(QtGui.QApplication.translate("DokumentDetailForm", "...", None, QtGui.QApplication.UnicodeUTF8))

from lib.ClickableLabel import ClickableLabel
