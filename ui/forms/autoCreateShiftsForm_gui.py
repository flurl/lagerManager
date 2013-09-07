# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/autoCreateShiftsForm.ui'
#
# Created: Sat Sep  7 18:49:17 2013
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

class Ui_AutoCreateShiftsForm(object):
    def setupUi(self, AutoCreateShiftsForm):
        AutoCreateShiftsForm.setObjectName(_fromUtf8("AutoCreateShiftsForm"))
        AutoCreateShiftsForm.resize(737, 430)
        self.verticalLayout = QtGui.QVBoxLayout(AutoCreateShiftsForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(AutoCreateShiftsForm)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.comboBox_recurrence = QtGui.QComboBox(self.tab)
        self.comboBox_recurrence.setObjectName(_fromUtf8("comboBox_recurrence"))
        self.comboBox_recurrence.addItem(_fromUtf8(""))
        self.comboBox_recurrence.addItem(_fromUtf8(""))
        self.comboBox_recurrence.addItem(_fromUtf8(""))
        self.comboBox_recurrence.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox_recurrence)
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_shiftName = QtGui.QLineEdit(self.tab)
        self.lineEdit_shiftName.setObjectName(_fromUtf8("lineEdit_shiftName"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_shiftName)
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_3)
        self.dateTimeEdit_shift = QtGui.QDateTimeEdit(self.tab)
        self.dateTimeEdit_shift.setCalendarPopup(True)
        self.dateTimeEdit_shift.setObjectName(_fromUtf8("dateTimeEdit_shift"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.dateTimeEdit_shift)
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.spinBox_recurrenceCount = QtGui.QSpinBox(self.tab)
        self.spinBox_recurrenceCount.setObjectName(_fromUtf8("spinBox_recurrenceCount"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.spinBox_recurrenceCount)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_5 = QtGui.QLabel(self.tab_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.radioButton_iCal = QtGui.QRadioButton(self.tab_2)
        self.radioButton_iCal.setObjectName(_fromUtf8("radioButton_iCal"))
        self.horizontalLayout.addWidget(self.radioButton_iCal)
        self.radioButton_RSS = QtGui.QRadioButton(self.tab_2)
        self.radioButton_RSS.setObjectName(_fromUtf8("radioButton_RSS"))
        self.horizontalLayout.addWidget(self.radioButton_RSS)
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_6 = QtGui.QLabel(self.tab_2)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_URL = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_URL.setObjectName(_fromUtf8("lineEdit_URL"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_URL)
        self.label_7 = QtGui.QLabel(self.tab_2)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_7)
        self.dateTimeEdit_ignoreBefore = QtGui.QDateTimeEdit(self.tab_2)
        self.dateTimeEdit_ignoreBefore.setCalendarPopup(True)
        self.dateTimeEdit_ignoreBefore.setObjectName(_fromUtf8("dateTimeEdit_ignoreBefore"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.dateTimeEdit_ignoreBefore)
        self.gridLayout_2.addLayout(self.formLayout_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_createShifts = QtGui.QPushButton(AutoCreateShiftsForm)
        self.pushButton_createShifts.setObjectName(_fromUtf8("pushButton_createShifts"))
        self.horizontalLayout_2.addWidget(self.pushButton_createShifts)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label.setBuddy(self.comboBox_recurrence)
        self.label_2.setBuddy(self.lineEdit_shiftName)
        self.label_3.setBuddy(self.dateTimeEdit_shift)
        self.label_4.setBuddy(self.spinBox_recurrenceCount)
        self.label_5.setBuddy(self.radioButton_iCal)
        self.label_6.setBuddy(self.lineEdit_URL)
        self.label_7.setBuddy(self.dateTimeEdit_ignoreBefore)

        self.retranslateUi(AutoCreateShiftsForm)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AutoCreateShiftsForm)
        AutoCreateShiftsForm.setTabOrder(self.comboBox_recurrence, self.spinBox_recurrenceCount)
        AutoCreateShiftsForm.setTabOrder(self.spinBox_recurrenceCount, self.lineEdit_shiftName)
        AutoCreateShiftsForm.setTabOrder(self.lineEdit_shiftName, self.dateTimeEdit_shift)

    def retranslateUi(self, AutoCreateShiftsForm):
        AutoCreateShiftsForm.setWindowTitle(_translate("AutoCreateShiftsForm", "Schichten erstellen", None))
        self.label.setText(_translate("AutoCreateShiftsForm", "&Wiederholung", None))
        self.comboBox_recurrence.setItemText(0, _translate("AutoCreateShiftsForm", "Täglich", None))
        self.comboBox_recurrence.setItemText(1, _translate("AutoCreateShiftsForm", "Wöchentlich", None))
        self.comboBox_recurrence.setItemText(2, _translate("AutoCreateShiftsForm", "Monatlich", None))
        self.comboBox_recurrence.setItemText(3, _translate("AutoCreateShiftsForm", "Jährlich", None))
        self.label_2.setText(_translate("AutoCreateShiftsForm", "Schicht &Bezeichnung", None))
        self.label_3.setText(_translate("AutoCreateShiftsForm", "Beginn &Datum/Zeit", None))
        self.label_4.setText(_translate("AutoCreateShiftsForm", "&Anzahl der Wiederholungen", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("AutoCreateShiftsForm", "Serie", None))
        self.label_5.setText(_translate("AutoCreateShiftsForm", "&Typ", None))
        self.radioButton_iCal.setText(_translate("AutoCreateShiftsForm", "iCal", None))
        self.radioButton_RSS.setText(_translate("AutoCreateShiftsForm", "RSS", None))
        self.label_6.setText(_translate("AutoCreateShiftsForm", "&URL", None))
        self.label_7.setText(_translate("AutoCreateShiftsForm", "&Ignoriere Schichten vor", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("AutoCreateShiftsForm", "Import", None))
        self.pushButton_createShifts.setText(_translate("AutoCreateShiftsForm", "&erstellen", None))

