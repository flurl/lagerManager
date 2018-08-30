# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/urlaubsanspruchReport.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_Urlaubsanspruch(object):
    def setupUi(self, Urlaubsanspruch):
        Urlaubsanspruch.setObjectName(_fromUtf8("Urlaubsanspruch"))
        Urlaubsanspruch.resize(881, 549)
        self.verticalLayout = QtGui.QVBoxLayout(Urlaubsanspruch)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBox_employees = QtGui.QComboBox(Urlaubsanspruch)
        self.comboBox_employees.setObjectName(_fromUtf8("comboBox_employees"))
        self.horizontalLayout.addWidget(self.comboBox_employees)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_export = QtGui.QPushButton(Urlaubsanspruch)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.pushButton_refresh = QtGui.QPushButton(Urlaubsanspruch)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.horizontalLayout.addWidget(self.pushButton_refresh)
        self.comboBox_period = QtGui.QComboBox(Urlaubsanspruch)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.textView = ReportTextViewWidget(Urlaubsanspruch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textView.sizePolicy().hasHeightForWidth())
        self.textView.setSizePolicy(sizePolicy)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.horizontalLayout_2.addWidget(self.textView)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Urlaubsanspruch)
        QtCore.QMetaObject.connectSlotsByName(Urlaubsanspruch)

    def retranslateUi(self, Urlaubsanspruch):
        Urlaubsanspruch.setWindowTitle(_translate("Urlaubsanspruch", "Urlaubsanspruch", None))
        self.pushButton_export.setText(_translate("Urlaubsanspruch", "&Exportieren", None))
        self.pushButton_refresh.setText(_translate("Urlaubsanspruch", "Aktualisieren", None))

from reports.reportTextViewWidget import ReportTextViewWidget
