# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/lagerstandReport.ui'
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

class Ui_Lagerstand(object):
    def setupUi(self, Lagerstand):
        Lagerstand.setObjectName(_fromUtf8("Lagerstand"))
        Lagerstand.resize(881, 549)
        self.verticalLayout = QtGui.QVBoxLayout(Lagerstand)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_refresh = QtGui.QPushButton(Lagerstand)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.horizontalLayout.addWidget(self.pushButton_refresh)
        self.comboBox_period = QtGui.QComboBox(Lagerstand)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_legend = QtGui.QVBoxLayout()
        self.verticalLayout_legend.setObjectName(_fromUtf8("verticalLayout_legend"))
        self.lineEdit_filterArticles = QtGui.QLineEdit(Lagerstand)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_filterArticles.sizePolicy().hasHeightForWidth())
        self.lineEdit_filterArticles.setSizePolicy(sizePolicy)
        self.lineEdit_filterArticles.setObjectName(_fromUtf8("lineEdit_filterArticles"))
        self.verticalLayout_legend.addWidget(self.lineEdit_filterArticles)
        self.scrollArea_articleSelection = QtGui.QScrollArea(Lagerstand)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_articleSelection.sizePolicy().hasHeightForWidth())
        self.scrollArea_articleSelection.setSizePolicy(sizePolicy)
        self.scrollArea_articleSelection.setWidgetResizable(True)
        self.scrollArea_articleSelection.setObjectName(_fromUtf8("scrollArea_articleSelection"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 424, 457))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.scrollArea_articleSelection.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_legend.addWidget(self.scrollArea_articleSelection)
        self.horizontalLayout_2.addLayout(self.verticalLayout_legend)
        self.graphicsView = ReportGraphicsViewWidget(Lagerstand)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout_2.addWidget(self.graphicsView)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Lagerstand)
        QtCore.QMetaObject.connectSlotsByName(Lagerstand)

    def retranslateUi(self, Lagerstand):
        Lagerstand.setWindowTitle(_translate("Lagerstand", "Lagerstand", None))
        self.pushButton_refresh.setText(_translate("Lagerstand", "Aktualisieren", None))

from reports.reportGraphicsViewWidget import ReportGraphicsViewWidget
