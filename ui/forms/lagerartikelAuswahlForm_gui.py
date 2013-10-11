# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/lagerartikelAuswahlForm.ui'
#
# Created: Fri Oct 11 12:42:35 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LagerartikelAuswahlForm(object):
    def setupUi(self, LagerartikelAuswahlForm):
        LagerartikelAuswahlForm.setObjectName(_fromUtf8("LagerartikelAuswahlForm"))
        LagerartikelAuswahlForm.resize(467, 284)
        self.gridLayout = QtGui.QGridLayout(LagerartikelAuswahlForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tableWidget_lagerartikel = QtGui.QTableWidget(LagerartikelAuswahlForm)
        self.tableWidget_lagerartikel.setObjectName(_fromUtf8("tableWidget_lagerartikel"))
        self.tableWidget_lagerartikel.setColumnCount(0)
        self.tableWidget_lagerartikel.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget_lagerartikel, 5, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.comboBox_period = QtGui.QComboBox(LagerartikelAuswahlForm)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout_2.addWidget(self.comboBox_period)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBox_artikelGruppen = QtGui.QComboBox(LagerartikelAuswahlForm)
        self.comboBox_artikelGruppen.setObjectName(_fromUtf8("comboBox_artikelGruppen"))
        self.horizontalLayout.addWidget(self.comboBox_artikelGruppen)
        self.pushButton_checkAll = QtGui.QPushButton(LagerartikelAuswahlForm)
        self.pushButton_checkAll.setObjectName(_fromUtf8("pushButton_checkAll"))
        self.horizontalLayout.addWidget(self.pushButton_checkAll)
        self.pushButton_uncheckAll = QtGui.QPushButton(LagerartikelAuswahlForm)
        self.pushButton_uncheckAll.setObjectName(_fromUtf8("pushButton_uncheckAll"))
        self.horizontalLayout.addWidget(self.pushButton_uncheckAll)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(LagerartikelAuswahlForm)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 1)

        self.retranslateUi(LagerartikelAuswahlForm)
        QtCore.QMetaObject.connectSlotsByName(LagerartikelAuswahlForm)

    def retranslateUi(self, LagerartikelAuswahlForm):
        LagerartikelAuswahlForm.setWindowTitle(QtGui.QApplication.translate("LagerartikelAuswahlForm", "Lagerartikel Auswahl", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_checkAll.setText(QtGui.QApplication.translate("LagerartikelAuswahlForm", "&Alle aktivieren", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_uncheckAll.setText(QtGui.QApplication.translate("LagerartikelAuswahlForm", "Alle &deaktivieren", None, QtGui.QApplication.UnicodeUTF8))

