# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/verprobungReport.ui'
#
# Created: Sun Jun 16 17:32:20 2013
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

class Ui_Verprobung(object):
    def setupUi(self, Verprobung):
        Verprobung.setObjectName(_fromUtf8("Verprobung"))
        Verprobung.resize(881, 549)
        self.verticalLayout = QtGui.QVBoxLayout(Verprobung)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_refresh = QtGui.QPushButton(Verprobung)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.horizontalLayout.addWidget(self.pushButton_refresh)
        self.comboBox_period = QtGui.QComboBox(Verprobung)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.groupBox = QtGui.QGroupBox(Verprobung)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.treeView_purchasesArticleGroups = QtGui.QTreeView(self.groupBox)
        self.treeView_purchasesArticleGroups.setObjectName(_fromUtf8("treeView_purchasesArticleGroups"))
        self.verticalLayout_4.addWidget(self.treeView_purchasesArticleGroups)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButton_purchasesCheckAll = QtGui.QPushButton(self.groupBox)
        self.pushButton_purchasesCheckAll.setObjectName(_fromUtf8("pushButton_purchasesCheckAll"))
        self.horizontalLayout_3.addWidget(self.pushButton_purchasesCheckAll)
        self.pushButton_purchasesUncheckAll = QtGui.QPushButton(self.groupBox)
        self.pushButton_purchasesUncheckAll.setObjectName(_fromUtf8("pushButton_purchasesUncheckAll"))
        self.horizontalLayout_3.addWidget(self.pushButton_purchasesUncheckAll)
        self.checkBox_purchasesFilter = QtGui.QCheckBox(self.groupBox)
        self.checkBox_purchasesFilter.setObjectName(_fromUtf8("checkBox_purchasesFilter"))
        self.horizontalLayout_3.addWidget(self.checkBox_purchasesFilter)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.lineEdit_purchasesFilter = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_purchasesFilter.setObjectName(_fromUtf8("lineEdit_purchasesFilter"))
        self.verticalLayout_4.addWidget(self.lineEdit_purchasesFilter)
        self.listView_purchasesArticles = QtGui.QListView(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.listView_purchasesArticles.sizePolicy().hasHeightForWidth())
        self.listView_purchasesArticles.setSizePolicy(sizePolicy)
        self.listView_purchasesArticles.setObjectName(_fromUtf8("listView_purchasesArticles"))
        self.verticalLayout_4.addWidget(self.listView_purchasesArticles)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(Verprobung)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.treeView_salesArticleGroups = QtGui.QTreeView(self.groupBox_2)
        self.treeView_salesArticleGroups.setObjectName(_fromUtf8("treeView_salesArticleGroups"))
        self.verticalLayout_2.addWidget(self.treeView_salesArticleGroups)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.pushButton_salesCheckAll = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_salesCheckAll.setObjectName(_fromUtf8("pushButton_salesCheckAll"))
        self.horizontalLayout_4.addWidget(self.pushButton_salesCheckAll)
        self.pushButton_salesUncheckAll = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_salesUncheckAll.setObjectName(_fromUtf8("pushButton_salesUncheckAll"))
        self.horizontalLayout_4.addWidget(self.pushButton_salesUncheckAll)
        self.checkBox_salesFilter = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_salesFilter.setObjectName(_fromUtf8("checkBox_salesFilter"))
        self.horizontalLayout_4.addWidget(self.checkBox_salesFilter)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.lineEdit_salesFilter = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_salesFilter.setObjectName(_fromUtf8("lineEdit_salesFilter"))
        self.verticalLayout_2.addWidget(self.lineEdit_salesFilter)
        self.listView_salesArticles = QtGui.QListView(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.listView_salesArticles.sizePolicy().hasHeightForWidth())
        self.listView_salesArticles.setSizePolicy(sizePolicy)
        self.listView_salesArticles.setObjectName(_fromUtf8("listView_salesArticles"))
        self.verticalLayout_2.addWidget(self.listView_salesArticles)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.textView = ReportTextViewWidget(Verprobung)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textView.sizePolicy().hasHeightForWidth())
        self.textView.setSizePolicy(sizePolicy)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.horizontalLayout_2.addWidget(self.textView)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Verprobung)
        QtCore.QMetaObject.connectSlotsByName(Verprobung)

    def retranslateUi(self, Verprobung):
        Verprobung.setWindowTitle(_translate("Verprobung", "Lagerstand", None))
        self.pushButton_refresh.setText(_translate("Verprobung", "Aktualisieren", None))
        self.groupBox.setTitle(_translate("Verprobung", "Einkauf", None))
        self.pushButton_purchasesCheckAll.setText(_translate("Verprobung", "Auswählen", None))
        self.pushButton_purchasesUncheckAll.setText(_translate("Verprobung", "Abwählen", None))
        self.checkBox_purchasesFilter.setText(_translate("Verprobung", "Filter", None))
        self.groupBox_2.setTitle(_translate("Verprobung", "Verkauf", None))
        self.pushButton_salesCheckAll.setText(_translate("Verprobung", "Auswählen", None))
        self.pushButton_salesUncheckAll.setText(_translate("Verprobung", "Abwählen", None))
        self.checkBox_salesFilter.setText(_translate("Verprobung", "Filter", None))

from reports.reportTextViewWidget import ReportTextViewWidget
