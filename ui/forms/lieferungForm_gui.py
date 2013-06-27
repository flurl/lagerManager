# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/lieferungForm.ui'
#
# Created: Thu Jun 27 16:55:39 2013
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

class Ui_LieferungForm(object):
    def setupUi(self, LieferungForm):
        LieferungForm.setObjectName(_fromUtf8("LieferungForm"))
        LieferungForm.resize(754, 451)
        self.gridLayout = QtGui.QGridLayout(LieferungForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(LieferungForm)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButton_new = QtGui.QPushButton(self.groupBox)
        self.pushButton_new.setObjectName(_fromUtf8("pushButton_new"))
        self.horizontalLayout_3.addWidget(self.pushButton_new)
        self.pushButton_edit = QtGui.QPushButton(self.groupBox)
        self.pushButton_edit.setObjectName(_fromUtf8("pushButton_edit"))
        self.horizontalLayout_3.addWidget(self.pushButton_edit)
        self.pushButton_delete = QtGui.QPushButton(self.groupBox)
        self.pushButton_delete.setObjectName(_fromUtf8("pushButton_delete"))
        self.horizontalLayout_3.addWidget(self.pushButton_delete)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.comboBox_period = QtGui.QComboBox(self.groupBox)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout_3.addWidget(self.comboBox_period)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.tableView_lieferungen = FilterableTableView(self.groupBox)
        self.tableView_lieferungen.setObjectName(_fromUtf8("tableView_lieferungen"))
        self.gridLayout_2.addWidget(self.tableView_lieferungen, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.radioButton_lieferung = QtGui.QRadioButton(self.groupBox)
        self.radioButton_lieferung.setChecked(True)
        self.radioButton_lieferung.setObjectName(_fromUtf8("radioButton_lieferung"))
        self.horizontalLayout_4.addWidget(self.radioButton_lieferung)
        self.radioButton_verbrauch = QtGui.QRadioButton(self.groupBox)
        self.radioButton_verbrauch.setObjectName(_fromUtf8("radioButton_verbrauch"))
        self.horizontalLayout_4.addWidget(self.radioButton_verbrauch)
        self.comboBox_filterArticle = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_filterArticle.sizePolicy().hasHeightForWidth())
        self.comboBox_filterArticle.setSizePolicy(sizePolicy)
        self.comboBox_filterArticle.setObjectName(_fromUtf8("comboBox_filterArticle"))
        self.horizontalLayout_4.addWidget(self.comboBox_filterArticle)
        self.checkBox_activateFilter = QtGui.QCheckBox(self.groupBox)
        self.checkBox_activateFilter.setObjectName(_fromUtf8("checkBox_activateFilter"))
        self.horizontalLayout_4.addWidget(self.checkBox_activateFilter)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.groupBox_2 = QtGui.QGroupBox(LieferungForm)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tableView_lieferungenDetails = QtGui.QTableView(self.groupBox_2)
        self.tableView_lieferungenDetails.setObjectName(_fromUtf8("tableView_lieferungenDetails"))
        self.gridLayout_3.addWidget(self.tableView_lieferungenDetails, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(LieferungForm)
        QtCore.QMetaObject.connectSlotsByName(LieferungForm)

    def retranslateUi(self, LieferungForm):
        LieferungForm.setWindowTitle(_translate("LieferungForm", "Form", None))
        self.pushButton_new.setText(_translate("LieferungForm", "&Neu", None))
        self.pushButton_edit.setText(_translate("LieferungForm", "&Bearbeiten", None))
        self.pushButton_delete.setText(_translate("LieferungForm", "&Löschen", None))
        self.radioButton_lieferung.setText(_translate("LieferungForm", "Lieferung", None))
        self.radioButton_verbrauch.setText(_translate("LieferungForm", "Verbrauch", None))
        self.checkBox_activateFilter.setText(_translate("LieferungForm", "&Filter aktivieren", None))
        self.groupBox_2.setTitle(_translate("LieferungForm", "Details", None))

from lib.FilterableTableView import FilterableTableView
