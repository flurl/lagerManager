# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/lieferungDetailForm.ui'
#
# Created: Fri May 17 22:18:13 2013
#      by: PyQt4 UI code generator 4.10
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

class Ui_LieferungDetailForm(object):
    def setupUi(self, LieferungDetailForm):
        LieferungDetailForm.setObjectName(_fromUtf8("LieferungDetailForm"))
        LieferungDetailForm.resize(687, 693)
        self.gridLayout = QtGui.QGridLayout(LieferungDetailForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_lieferung = QtGui.QGroupBox(LieferungDetailForm)
        self.groupBox_lieferung.setObjectName(_fromUtf8("groupBox_lieferung"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_lieferung)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupBox_lieferung)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEdit_id = QtGui.QLineEdit(self.groupBox_lieferung)
        self.lineEdit_id.setReadOnly(True)
        self.lineEdit_id.setObjectName(_fromUtf8("lineEdit_id"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_id)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.plainTextEdit_comment = QtGui.QPlainTextEdit(self.groupBox_lieferung)
        self.plainTextEdit_comment.setObjectName(_fromUtf8("plainTextEdit_comment"))
        self.horizontalLayout_4.addWidget(self.plainTextEdit_comment)
        self.formLayout.setLayout(4, QtGui.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label_4 = QtGui.QLabel(self.groupBox_lieferung)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_4)
        self.layout_documents = QtGui.QHBoxLayout()
        self.layout_documents.setObjectName(_fromUtf8("layout_documents"))
        self.pushButton_addDocument = QtGui.QPushButton(self.groupBox_lieferung)
        self.pushButton_addDocument.setObjectName(_fromUtf8("pushButton_addDocument"))
        self.layout_documents.addWidget(self.pushButton_addDocument)
        self.formLayout.setLayout(7, QtGui.QFormLayout.FieldRole, self.layout_documents)
        self.label_6 = QtGui.QLabel(self.groupBox_lieferung)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_6)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.comboBox_lieferant = QtGui.QComboBox(self.groupBox_lieferung)
        self.comboBox_lieferant.setObjectName(_fromUtf8("comboBox_lieferant"))
        self.horizontalLayout_5.addWidget(self.comboBox_lieferant)
        self.label_3 = QtGui.QLabel(self.groupBox_lieferung)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_5.addWidget(self.label_3)
        self.dateEdit_datum = QtGui.QDateEdit(self.groupBox_lieferung)
        self.dateEdit_datum.setCalendarPopup(True)
        self.dateEdit_datum.setObjectName(_fromUtf8("dateEdit_datum"))
        self.horizontalLayout_5.addWidget(self.dateEdit_datum)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label_lieferant = QtGui.QLabel(self.groupBox_lieferung)
        self.label_lieferant.setObjectName(_fromUtf8("label_lieferant"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_lieferant)
        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_lieferung, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(LieferungDetailForm)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(LieferungDetailForm)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_newDetail = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_newDetail.setObjectName(_fromUtf8("pushButton_newDetail"))
        self.horizontalLayout.addWidget(self.pushButton_newDetail)
        self.pushButton_deleteDetail = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_deleteDetail.setObjectName(_fromUtf8("pushButton_deleteDetail"))
        self.horizontalLayout.addWidget(self.pushButton_deleteDetail)
        self.pushButton_selectArticles = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_selectArticles.setObjectName(_fromUtf8("pushButton_selectArticles"))
        self.horizontalLayout.addWidget(self.pushButton_selectArticles)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView_details = QtGui.QTableView(self.groupBox_2)
        self.tableView_details.setObjectName(_fromUtf8("tableView_details"))
        self.verticalLayout.addWidget(self.tableView_details)
        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 1)

        self.retranslateUi(LieferungDetailForm)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LieferungDetailForm.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LieferungDetailForm.reject)
        QtCore.QMetaObject.connectSlotsByName(LieferungDetailForm)

    def retranslateUi(self, LieferungDetailForm):
        LieferungDetailForm.setWindowTitle(_translate("LieferungDetailForm", "Dialog", None))
        self.groupBox_lieferung.setTitle(_translate("LieferungDetailForm", "Lieferung", None))
        self.label.setText(_translate("LieferungDetailForm", "ID", None))
        self.label_4.setText(_translate("LieferungDetailForm", "Dokumente", None))
        self.pushButton_addDocument.setText(_translate("LieferungDetailForm", "+", None))
        self.label_6.setText(_translate("LieferungDetailForm", "Kommentar", None))
        self.label_3.setText(_translate("LieferungDetailForm", "Datum", None))
        self.label_lieferant.setText(_translate("LieferungDetailForm", "Lieferant", None))
        self.groupBox_2.setTitle(_translate("LieferungDetailForm", "Details", None))
        self.pushButton_newDetail.setText(_translate("LieferungDetailForm", "&Hinzufügen", None))
        self.pushButton_deleteDetail.setText(_translate("LieferungDetailForm", "&Löschen", None))
        self.pushButton_selectArticles.setText(_translate("LieferungDetailForm", "&Artikelauswahl", None))

import lagerManager_rc
