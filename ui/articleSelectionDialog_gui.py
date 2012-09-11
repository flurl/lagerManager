# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/articleSelectionDialog.ui'
#
# Created: Thu Apr  2 07:21:12 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ArticleSelectionDialog(object):
    def setupUi(self, ArticleSelectionDialog):
        ArticleSelectionDialog.setObjectName("ArticleSelectionDialog")
        ArticleSelectionDialog.resize(416,464)
        self.gridLayout = QtGui.QGridLayout(ArticleSelectionDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget_articles = QtGui.QTableWidget(ArticleSelectionDialog)
        self.tableWidget_articles.setObjectName("tableWidget_articles")
        self.gridLayout.addWidget(self.tableWidget_articles,0,0,1,1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_ok = QtGui.QPushButton(ArticleSelectionDialog)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.pushButton_set = QtGui.QPushButton(ArticleSelectionDialog)
        self.pushButton_set.setObjectName("pushButton_set")
        self.horizontalLayout.addWidget(self.pushButton_set)
        self.pushButton_checkAll = QtGui.QPushButton(ArticleSelectionDialog)
        self.pushButton_checkAll.setObjectName("pushButton_checkAll")
        self.horizontalLayout.addWidget(self.pushButton_checkAll)
        self.pushButton_uncheckAll = QtGui.QPushButton(ArticleSelectionDialog)
        self.pushButton_uncheckAll.setObjectName("pushButton_uncheckAll")
        self.horizontalLayout.addWidget(self.pushButton_uncheckAll)
        self.gridLayout.addLayout(self.horizontalLayout,1,0,1,1)

        self.retranslateUi(ArticleSelectionDialog)
        QtCore.QMetaObject.connectSlotsByName(ArticleSelectionDialog)

    def retranslateUi(self, ArticleSelectionDialog):
        ArticleSelectionDialog.setWindowTitle(QtGui.QApplication.translate("ArticleSelectionDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget_articles.clear()
        self.tableWidget_articles.setColumnCount(0)
        self.tableWidget_articles.setRowCount(0)
        self.pushButton_ok.setText(QtGui.QApplication.translate("ArticleSelectionDialog", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_set.setText(QtGui.QApplication.translate("ArticleSelectionDialog", "&Set", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_checkAll.setText(QtGui.QApplication.translate("ArticleSelectionDialog", "&Check All", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_uncheckAll.setText(QtGui.QApplication.translate("ArticleSelectionDialog", "&Uncheck All", None, QtGui.QApplication.UnicodeUTF8))

