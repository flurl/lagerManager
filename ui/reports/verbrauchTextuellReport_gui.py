# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/verbrauchTextuellReport.ui'
#
# Created: Thu Jul 30 18:55:34 2015
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

class Ui_VerbrauchTextuellReport(object):
    def setupUi(self, VerbrauchTextuellReport):
        VerbrauchTextuellReport.setObjectName(_fromUtf8("VerbrauchTextuellReport"))
        VerbrauchTextuellReport.resize(989, 500)
        self.gridLayout = QtGui.QGridLayout(VerbrauchTextuellReport)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBox_useTillDate = QtGui.QCheckBox(VerbrauchTextuellReport)
        self.checkBox_useTillDate.setObjectName(_fromUtf8("checkBox_useTillDate"))
        self.horizontalLayout.addWidget(self.checkBox_useTillDate)
        self.dateEdit_till = QtGui.QDateEdit(VerbrauchTextuellReport)
        self.dateEdit_till.setCalendarPopup(True)
        self.dateEdit_till.setObjectName(_fromUtf8("dateEdit_till"))
        self.horizontalLayout.addWidget(self.dateEdit_till)
        self.radioButton_all = QtGui.QRadioButton(VerbrauchTextuellReport)
        self.radioButton_all.setChecked(True)
        self.radioButton_all.setObjectName(_fromUtf8("radioButton_all"))
        self.horizontalLayout.addWidget(self.radioButton_all)
        self.radioButton_umsatz = QtGui.QRadioButton(VerbrauchTextuellReport)
        self.radioButton_umsatz.setObjectName(_fromUtf8("radioButton_umsatz"))
        self.horizontalLayout.addWidget(self.radioButton_umsatz)
        self.radioButton_aufwand = QtGui.QRadioButton(VerbrauchTextuellReport)
        self.radioButton_aufwand.setObjectName(_fromUtf8("radioButton_aufwand"))
        self.horizontalLayout.addWidget(self.radioButton_aufwand)
        self.checkBox_showTableCode = QtGui.QCheckBox(VerbrauchTextuellReport)
        self.checkBox_showTableCode.setObjectName(_fromUtf8("checkBox_showTableCode"))
        self.horizontalLayout.addWidget(self.checkBox_showTableCode)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_export = QtGui.QPushButton(VerbrauchTextuellReport)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.comboBox_period = QtGui.QComboBox(VerbrauchTextuellReport)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textView = ReportTextViewWidget(VerbrauchTextuellReport)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.verticalLayout.addWidget(self.textView)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.retranslateUi(VerbrauchTextuellReport)
        QtCore.QMetaObject.connectSlotsByName(VerbrauchTextuellReport)

    def retranslateUi(self, VerbrauchTextuellReport):
        VerbrauchTextuellReport.setWindowTitle(_translate("VerbrauchTextuellReport", "Verbrauch", None))
        self.checkBox_useTillDate.setText(_translate("VerbrauchTextuellReport", "Daten berücksichtigen &nur bis zum ", None))
        self.radioButton_all.setText(_translate("VerbrauchTextuellReport", "&Alles", None))
        self.radioButton_umsatz.setText(_translate("VerbrauchTextuellReport", "nur &Umsatz", None))
        self.radioButton_aufwand.setText(_translate("VerbrauchTextuellReport", "nur Auf&wand", None))
        self.checkBox_showTableCode.setText(_translate("VerbrauchTextuellReport", "&Tischbereiche anzeigen", None))
        self.pushButton_export.setText(_translate("VerbrauchTextuellReport", "&Exportieren", None))

from reports.reportTextViewWidget import ReportTextViewWidget
