# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/durchschnittUmsatzProTag.ui'
#
# Created: Tue Aug 12 18:12:34 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_DurchschnittUmsatzProTag(object):
    def setupUi(self, DurchschnittUmsatzProTag):
        DurchschnittUmsatzProTag.setObjectName(_fromUtf8("DurchschnittUmsatzProTag"))
        DurchschnittUmsatzProTag.resize(989, 500)
        self.gridLayout = QtGui.QGridLayout(DurchschnittUmsatzProTag)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBox_listHours = QtGui.QCheckBox(DurchschnittUmsatzProTag)
        self.checkBox_listHours.setObjectName(_fromUtf8("checkBox_listHours"))
        self.horizontalLayout.addWidget(self.checkBox_listHours)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_export = QtGui.QPushButton(DurchschnittUmsatzProTag)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.comboBox_period = QtGui.QComboBox(DurchschnittUmsatzProTag)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textView = ReportTextViewWidget(DurchschnittUmsatzProTag)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.verticalLayout.addWidget(self.textView)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.retranslateUi(DurchschnittUmsatzProTag)
        QtCore.QMetaObject.connectSlotsByName(DurchschnittUmsatzProTag)

    def retranslateUi(self, DurchschnittUmsatzProTag):
        DurchschnittUmsatzProTag.setWindowTitle(_translate("DurchschnittUmsatzProTag", "Durchnschnittlicher Umsatz pro Wochentag", None))
        self.checkBox_listHours.setText(_translate("DurchschnittUmsatzProTag", "&Stunden auflisten", None))
        self.pushButton_export.setText(_translate("DurchschnittUmsatzProTag", "&Exportieren", None))

from reports.reportTextViewWidget import ReportTextViewWidget
