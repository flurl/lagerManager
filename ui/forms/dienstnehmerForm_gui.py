# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/dienstnehmerForm.ui'
#
# Created: Tue Jun 18 15:49:20 2013
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

class Ui_DienstnehmerForm(object):
    def setupUi(self, DienstnehmerForm):
        DienstnehmerForm.setObjectName(_fromUtf8("DienstnehmerForm"))
        DienstnehmerForm.resize(662, 287)
        self.gridLayout = QtGui.QGridLayout(DienstnehmerForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_newRecord = QtGui.QPushButton(DienstnehmerForm)
        self.pushButton_newRecord.setObjectName(_fromUtf8("pushButton_newRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_newRecord)
        self.pushButton_deleteRecord = QtGui.QPushButton(DienstnehmerForm)
        self.pushButton_deleteRecord.setObjectName(_fromUtf8("pushButton_deleteRecord"))
        self.horizontalLayout_2.addWidget(self.pushButton_deleteRecord)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.comboBox_period = QtGui.QComboBox(DienstnehmerForm)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout_2.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 2)
        self.tableView_dienstnehmer = QtGui.QTableView(DienstnehmerForm)
        self.tableView_dienstnehmer.setObjectName(_fromUtf8("tableView_dienstnehmer"))
        self.gridLayout.addWidget(self.tableView_dienstnehmer, 2, 0, 1, 1)

        self.retranslateUi(DienstnehmerForm)
        QtCore.QMetaObject.connectSlotsByName(DienstnehmerForm)

    def retranslateUi(self, DienstnehmerForm):
        DienstnehmerForm.setWindowTitle(_translate("DienstnehmerForm", "Dialog", None))
        self.pushButton_newRecord.setText(_translate("DienstnehmerForm", "&Neu", None))
        self.pushButton_deleteRecord.setText(_translate("DienstnehmerForm", "&Löschen", None))

