# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/dokumentDetailForm.ui'
#
# Created: Fri Oct 11 12:43:32 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DokumentDetailForm(object):
    def setupUi(self, DokumentDetailForm):
        DokumentDetailForm.setObjectName(_fromUtf8("DokumentDetailForm"))
        DokumentDetailForm.resize(515, 479)
        self.gridLayout = QtGui.QGridLayout(DokumentDetailForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(DokumentDetailForm)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_id = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_id.setReadOnly(True)
        self.lineEdit_id.setObjectName(_fromUtf8("lineEdit_id"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_id)
        self.comboBox_typ = QtGui.QComboBox(self.groupBox)
        self.comboBox_typ.setObjectName(_fromUtf8("comboBox_typ"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBox_typ)
        self.dateEdit_datum = QtGui.QDateEdit(self.groupBox)
        self.dateEdit_datum.setCalendarPopup(True)
        self.dateEdit_datum.setObjectName(_fromUtf8("dateEdit_datum"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.dateEdit_datum)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_fileChooser = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_fileChooser.sizePolicy().hasHeightForWidth())
        self.pushButton_fileChooser.setSizePolicy(sizePolicy)
        self.pushButton_fileChooser.setObjectName(_fromUtf8("pushButton_fileChooser"))
        self.horizontalLayout_2.addWidget(self.pushButton_fileChooser)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.formLayout.setLayout(5, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.lineEdit_bezeichnung = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_bezeichnung.setObjectName(_fromUtf8("lineEdit_bezeichnung"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_bezeichnung)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_6)
        self.plainTextEdit_ocr = QtGui.QPlainTextEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit_ocr.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_ocr.setSizePolicy(sizePolicy)
        self.plainTextEdit_ocr.setMinimumSize(QtCore.QSize(0, 200))
        self.plainTextEdit_ocr.setObjectName(_fromUtf8("plainTextEdit_ocr"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.plainTextEdit_ocr)
        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)
        self.label_documentImage = ClickableLabel(self.groupBox)
        self.label_documentImage.setText(_fromUtf8(""))
        self.label_documentImage.setObjectName(_fromUtf8("label_documentImage"))
        self.gridLayout_2.addWidget(self.label_documentImage, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DokumentDetailForm)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(DokumentDetailForm)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DokumentDetailForm.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DokumentDetailForm.reject)
        QtCore.QMetaObject.connectSlotsByName(DokumentDetailForm)

    def retranslateUi(self, DokumentDetailForm):
        DokumentDetailForm.setWindowTitle(QtGui.QApplication.translate("DokumentDetailForm", "Dokument Details", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("DokumentDetailForm", "Lieferung", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DokumentDetailForm", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DokumentDetailForm", "Typ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DokumentDetailForm", "Datum", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("DokumentDetailForm", "Datei", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_fileChooser.setText(QtGui.QApplication.translate("DokumentDetailForm", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("DokumentDetailForm", "Bezeichnung", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("DokumentDetailForm", "Text", None, QtGui.QApplication.UnicodeUTF8))

from lib.ClickableLabel import ClickableLabel
