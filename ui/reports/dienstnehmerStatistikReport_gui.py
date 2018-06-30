# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/dienstnehmerStatistikReport.ui'
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

class Ui_DienstnehmerStatistik(object):
    def setupUi(self, DienstnehmerStatistik):
        DienstnehmerStatistik.setObjectName(_fromUtf8("DienstnehmerStatistik"))
        DienstnehmerStatistik.resize(881, 549)
        self.verticalLayout = QtGui.QVBoxLayout(DienstnehmerStatistik)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBox_employees = QtGui.QComboBox(DienstnehmerStatistik)
        self.comboBox_employees.setObjectName(_fromUtf8("comboBox_employees"))
        self.horizontalLayout.addWidget(self.comboBox_employees)
        self.comboBox_calculationPeriod = QtGui.QComboBox(DienstnehmerStatistik)
        self.comboBox_calculationPeriod.setObjectName(_fromUtf8("comboBox_calculationPeriod"))
        self.comboBox_calculationPeriod.addItem(_fromUtf8(""))
        self.comboBox_calculationPeriod.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox_calculationPeriod)
        self.comboBox_periodAmount = QtGui.QComboBox(DienstnehmerStatistik)
        self.comboBox_periodAmount.setObjectName(_fromUtf8("comboBox_periodAmount"))
        self.horizontalLayout.addWidget(self.comboBox_periodAmount)
        self.checkBox_singlePeriods = QtGui.QCheckBox(DienstnehmerStatistik)
        self.checkBox_singlePeriods.setObjectName(_fromUtf8("checkBox_singlePeriods"))
        self.horizontalLayout.addWidget(self.checkBox_singlePeriods)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_export = QtGui.QPushButton(DienstnehmerStatistik)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.pushButton_refresh = QtGui.QPushButton(DienstnehmerStatistik)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.horizontalLayout.addWidget(self.pushButton_refresh)
        self.comboBox_period = QtGui.QComboBox(DienstnehmerStatistik)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.textView = ReportTextViewWidget(DienstnehmerStatistik)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textView.sizePolicy().hasHeightForWidth())
        self.textView.setSizePolicy(sizePolicy)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.horizontalLayout_2.addWidget(self.textView)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(DienstnehmerStatistik)
        QtCore.QMetaObject.connectSlotsByName(DienstnehmerStatistik)

    def retranslateUi(self, DienstnehmerStatistik):
        DienstnehmerStatistik.setWindowTitle(_translate("DienstnehmerStatistik", "Dienstnehmer Stunden", None))
        self.comboBox_calculationPeriod.setItemText(0, _translate("DienstnehmerStatistik", "Weekly", None))
        self.comboBox_calculationPeriod.setItemText(1, _translate("DienstnehmerStatistik", "Monthly", None))
        self.checkBox_singlePeriods.setText(_translate("DienstnehmerStatistik", "einzelne &Zeiträume", None))
        self.pushButton_export.setText(_translate("DienstnehmerStatistik", "&Exportieren", None))
        self.pushButton_refresh.setText(_translate("DienstnehmerStatistik", "Aktualisieren", None))

from reports.reportTextViewWidget import ReportTextViewWidget
