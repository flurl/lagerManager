# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/dienstnehmerStundenReport.ui'
#
# Created: Mon Sep  2 16:17:12 2013
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

class Ui_DienstnehmerStunden(object):
    def setupUi(self, DienstnehmerStunden):
        DienstnehmerStunden.setObjectName(_fromUtf8("DienstnehmerStunden"))
        DienstnehmerStunden.resize(881, 549)
        self.verticalLayout = QtGui.QVBoxLayout(DienstnehmerStunden)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBox_reportType = QtGui.QComboBox(DienstnehmerStunden)
        self.comboBox_reportType.setObjectName(_fromUtf8("comboBox_reportType"))
        self.comboBox_reportType.addItem(_fromUtf8(""))
        self.comboBox_reportType.addItem(_fromUtf8(""))
        self.comboBox_reportType.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox_reportType)
        self.comboBox_employees = QtGui.QComboBox(DienstnehmerStunden)
        self.comboBox_employees.setObjectName(_fromUtf8("comboBox_employees"))
        self.horizontalLayout.addWidget(self.comboBox_employees)
        self.comboBox_fieldOfEmployment = QtGui.QComboBox(DienstnehmerStunden)
        self.comboBox_fieldOfEmployment.setObjectName(_fromUtf8("comboBox_fieldOfEmployment"))
        self.horizontalLayout.addWidget(self.comboBox_fieldOfEmployment)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_export = QtGui.QPushButton(DienstnehmerStunden)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.pushButton_refresh = QtGui.QPushButton(DienstnehmerStunden)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.horizontalLayout.addWidget(self.pushButton_refresh)
        self.comboBox_period = QtGui.QComboBox(DienstnehmerStunden)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.textView = ReportTextViewWidget(DienstnehmerStunden)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textView.sizePolicy().hasHeightForWidth())
        self.textView.setSizePolicy(sizePolicy)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.horizontalLayout_2.addWidget(self.textView)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(DienstnehmerStunden)
        QtCore.QMetaObject.connectSlotsByName(DienstnehmerStunden)

    def retranslateUi(self, DienstnehmerStunden):
        DienstnehmerStunden.setWindowTitle(_translate("DienstnehmerStunden", "Dienstnehmer Stunden", None))
        self.comboBox_reportType.setItemText(0, _translate("DienstnehmerStunden", "Jährlich", None))
        self.comboBox_reportType.setItemText(1, _translate("DienstnehmerStunden", "Monatlich", None))
        self.comboBox_reportType.setItemText(2, _translate("DienstnehmerStunden", "Täglich", None))
        self.pushButton_export.setText(_translate("DienstnehmerStunden", "&Exportieren", None))
        self.pushButton_refresh.setText(_translate("DienstnehmerStunden", "Aktualisieren", None))

from reports.reportTextViewWidget import ReportTextViewWidget
