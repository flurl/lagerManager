# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/aufwandDetailsProTag.ui'
#
# Created: Sat Feb 23 22:58:44 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AufwandDetailsProTagReport(object):
    def setupUi(self, AufwandDetailsProTagReport):
        AufwandDetailsProTagReport.setObjectName(_fromUtf8("AufwandDetailsProTagReport"))
        AufwandDetailsProTagReport.resize(747, 519)
        self.gridLayout = QtGui.QGridLayout(AufwandDetailsProTagReport)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.comboBox_period = QtGui.QComboBox(AufwandDetailsProTagReport)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lineEdit_filterArticles = QtGui.QLineEdit(AufwandDetailsProTagReport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_filterArticles.sizePolicy().hasHeightForWidth())
        self.lineEdit_filterArticles.setSizePolicy(sizePolicy)
        self.lineEdit_filterArticles.setObjectName(_fromUtf8("lineEdit_filterArticles"))
        self.verticalLayout_2.addWidget(self.lineEdit_filterArticles)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(AufwandDetailsProTagReport)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.dateEdit_from = QtGui.QDateEdit(AufwandDetailsProTagReport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit_from.sizePolicy().hasHeightForWidth())
        self.dateEdit_from.setSizePolicy(sizePolicy)
        self.dateEdit_from.setCalendarPopup(True)
        self.dateEdit_from.setObjectName(_fromUtf8("dateEdit_from"))
        self.horizontalLayout_3.addWidget(self.dateEdit_from)
        self.label_2 = QtGui.QLabel(AufwandDetailsProTagReport)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.dateEdit_till = QtGui.QDateEdit(AufwandDetailsProTagReport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit_till.sizePolicy().hasHeightForWidth())
        self.dateEdit_till.setSizePolicy(sizePolicy)
        self.dateEdit_till.setCalendarPopup(True)
        self.dateEdit_till.setObjectName(_fromUtf8("dateEdit_till"))
        self.horizontalLayout_3.addWidget(self.dateEdit_till)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.checkBox_zeroBonierungen = QtGui.QCheckBox(AufwandDetailsProTagReport)
        self.checkBox_zeroBonierungen.setObjectName(_fromUtf8("checkBox_zeroBonierungen"))
        self.horizontalLayout_4.addWidget(self.checkBox_zeroBonierungen)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.textView = ReportTextViewWidget(AufwandDetailsProTagReport)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.horizontalLayout_2.addWidget(self.textView)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.retranslateUi(AufwandDetailsProTagReport)
        QtCore.QMetaObject.connectSlotsByName(AufwandDetailsProTagReport)

    def retranslateUi(self, AufwandDetailsProTagReport):
        AufwandDetailsProTagReport.setWindowTitle(QtGui.QApplication.translate("AufwandDetailsProTagReport", "Report", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AufwandDetailsProTagReport", "von", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("AufwandDetailsProTagReport", "bis", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_zeroBonierungen.setText(QtGui.QApplication.translate("AufwandDetailsProTagReport", "0€ Bonierungen berücksichtigen", None, QtGui.QApplication.UnicodeUTF8))

from reports.reportTextViewWidget import ReportTextViewWidget
