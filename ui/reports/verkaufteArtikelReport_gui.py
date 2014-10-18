# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/verkaufteArtikelReport.ui'
#
# Created: Sat Oct 18 18:05:26 2014
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

class Ui_VerkaufteArtikelReport(object):
    def setupUi(self, VerkaufteArtikelReport):
        VerkaufteArtikelReport.setObjectName(_fromUtf8("VerkaufteArtikelReport"))
        VerkaufteArtikelReport.resize(1096, 500)
        self.gridLayout = QtGui.QGridLayout(VerkaufteArtikelReport)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(VerkaufteArtikelReport)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_checkpoint = QtGui.QComboBox(VerkaufteArtikelReport)
        self.comboBox_checkpoint.setObjectName(_fromUtf8("comboBox_checkpoint"))
        self.horizontalLayout.addWidget(self.comboBox_checkpoint)
        self.radioButton_all = QtGui.QRadioButton(VerkaufteArtikelReport)
        self.radioButton_all.setChecked(True)
        self.radioButton_all.setObjectName(_fromUtf8("radioButton_all"))
        self.horizontalLayout.addWidget(self.radioButton_all)
        self.radioButton_umsatz = QtGui.QRadioButton(VerkaufteArtikelReport)
        self.radioButton_umsatz.setObjectName(_fromUtf8("radioButton_umsatz"))
        self.horizontalLayout.addWidget(self.radioButton_umsatz)
        self.radioButton_aufwand = QtGui.QRadioButton(VerkaufteArtikelReport)
        self.radioButton_aufwand.setObjectName(_fromUtf8("radioButton_aufwand"))
        self.horizontalLayout.addWidget(self.radioButton_aufwand)
        self.checkBox_showTableCode = QtGui.QCheckBox(VerkaufteArtikelReport)
        self.checkBox_showTableCode.setObjectName(_fromUtf8("checkBox_showTableCode"))
        self.horizontalLayout.addWidget(self.checkBox_showTableCode)
        self.checkBox_showDate = QtGui.QCheckBox(VerkaufteArtikelReport)
        self.checkBox_showDate.setObjectName(_fromUtf8("checkBox_showDate"))
        self.horizontalLayout.addWidget(self.checkBox_showDate)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_export = QtGui.QPushButton(VerkaufteArtikelReport)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.comboBox_period = QtGui.QComboBox(VerkaufteArtikelReport)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textView = ReportTextViewWidget(VerkaufteArtikelReport)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.verticalLayout.addWidget(self.textView)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.retranslateUi(VerkaufteArtikelReport)
        QtCore.QMetaObject.connectSlotsByName(VerkaufteArtikelReport)

    def retranslateUi(self, VerkaufteArtikelReport):
        VerkaufteArtikelReport.setWindowTitle(_translate("VerkaufteArtikelReport", "Verkaufte Artikel", None))
        self.label.setText(_translate("VerkaufteArtikelReport", "&Checkpoint", None))
        self.radioButton_all.setText(_translate("VerkaufteArtikelReport", "&Alles", None))
        self.radioButton_umsatz.setText(_translate("VerkaufteArtikelReport", "nur &Umsatz", None))
        self.radioButton_aufwand.setText(_translate("VerkaufteArtikelReport", "nur Auf&wand", None))
        self.checkBox_showTableCode.setText(_translate("VerkaufteArtikelReport", "&Tischbereiche anzeigen", None))
        self.checkBox_showDate.setText(_translate("VerkaufteArtikelReport", "&Datum anzeigen", None))
        self.pushButton_export.setText(_translate("VerkaufteArtikelReport", "&Exportieren", None))

from reports.reportTextViewWidget import ReportTextViewWidget
