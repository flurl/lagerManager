# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/verbrauchReport.ui'
#
# Created: Thu Sep  6 04:17:29 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Verbrauch(object):
    def setupUi(self, Verbrauch):
        Verbrauch.setObjectName(_fromUtf8("Verbrauch"))
        Verbrauch.resize(881, 549)
        self.verticalLayout = QtGui.QVBoxLayout(Verbrauch)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_refresh = QtGui.QPushButton(Verbrauch)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.horizontalLayout.addWidget(self.pushButton_refresh)
        self.comboBox_period = QtGui.QComboBox(Verbrauch)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lineEdit_filterArticles = QtGui.QLineEdit(Verbrauch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_filterArticles.sizePolicy().hasHeightForWidth())
        self.lineEdit_filterArticles.setSizePolicy(sizePolicy)
        self.lineEdit_filterArticles.setObjectName(_fromUtf8("lineEdit_filterArticles"))
        self.verticalLayout_2.addWidget(self.lineEdit_filterArticles)
        self.scrollArea_articleSelection = QtGui.QScrollArea(Verbrauch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_articleSelection.sizePolicy().hasHeightForWidth())
        self.scrollArea_articleSelection.setSizePolicy(sizePolicy)
        self.scrollArea_articleSelection.setWidgetResizable(True)
        self.scrollArea_articleSelection.setObjectName(_fromUtf8("scrollArea_articleSelection"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 426, 474))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.scrollArea_articleSelection.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea_articleSelection)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.graphicsView = ReportGraphicsViewWidget(Verbrauch)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout_2.addWidget(self.graphicsView)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Verbrauch)
        QtCore.QMetaObject.connectSlotsByName(Verbrauch)

    def retranslateUi(self, Verbrauch):
        Verbrauch.setWindowTitle(QtGui.QApplication.translate("Verbrauch", "Verbrauch", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_refresh.setText(QtGui.QApplication.translate("Verbrauch", "Aktualisieren", None, QtGui.QApplication.UnicodeUTF8))

from reports.reportGraphicsViewWidget import ReportGraphicsViewWidget
