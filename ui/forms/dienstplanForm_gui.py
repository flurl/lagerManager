# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/dienstplanForm.ui'
#
# Created: Wed Oct 23 18:33:42 2013
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

class Ui_DienstplanForm(object):
    def setupUi(self, DienstplanForm):
        DienstplanForm.setObjectName(_fromUtf8("DienstplanForm"))
        DienstplanForm.resize(1176, 729)
        self.gridLayout_2 = QtGui.QGridLayout(DienstplanForm)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(DienstplanForm)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_event = LMComboBox(DienstplanForm)
        self.comboBox_event.setObjectName(_fromUtf8("comboBox_event"))
        self.horizontalLayout.addWidget(self.comboBox_event)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_refresh = QtGui.QPushButton(DienstplanForm)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.horizontalLayout.addWidget(self.pushButton_refresh)
        self.comboBox_period = QtGui.QComboBox(DienstplanForm)
        self.comboBox_period.setObjectName(_fromUtf8("comboBox_period"))
        self.horizontalLayout.addWidget(self.comboBox_period)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(DienstplanForm)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.comboBox_template = QtGui.QComboBox(DienstplanForm)
        self.comboBox_template.setObjectName(_fromUtf8("comboBox_template"))
        self.horizontalLayout_3.addWidget(self.comboBox_template)
        self.pushButton_loadTemplate = QtGui.QPushButton(DienstplanForm)
        self.pushButton_loadTemplate.setObjectName(_fromUtf8("pushButton_loadTemplate"))
        self.horizontalLayout_3.addWidget(self.pushButton_loadTemplate)
        self.pushButton_saveTemplate = QtGui.QPushButton(DienstplanForm)
        self.pushButton_saveTemplate.setObjectName(_fromUtf8("pushButton_saveTemplate"))
        self.horizontalLayout_3.addWidget(self.pushButton_saveTemplate)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.pushButton_autoAssignEmps = QtGui.QPushButton(DienstplanForm)
        self.pushButton_autoAssignEmps.setObjectName(_fromUtf8("pushButton_autoAssignEmps"))
        self.horizontalLayout_3.addWidget(self.pushButton_autoAssignEmps)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.groupBox_event = QtGui.QGroupBox(DienstplanForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.groupBox_event.sizePolicy().hasHeightForWidth())
        self.groupBox_event.setSizePolicy(sizePolicy)
        self.groupBox_event.setObjectName(_fromUtf8("groupBox_event"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_event)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.scrollArea = QtGui.QScrollArea(self.groupBox_event)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1148, 572))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_employees = QtGui.QVBoxLayout()
        self.verticalLayout_employees.setObjectName(_fromUtf8("verticalLayout_employees"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.pushButton_addEmployee = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_addEmployee.setObjectName(_fromUtf8("pushButton_addEmployee"))
        self.horizontalLayout_8.addWidget(self.pushButton_addEmployee)
        self.pushButton_sort = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_sort.setObjectName(_fromUtf8("pushButton_sort"))
        self.horizontalLayout_8.addWidget(self.pushButton_sort)
        self.verticalLayout_employees.addLayout(self.horizontalLayout_8)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_employees.addItem(spacerItem2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_employees)
        self.graphicsView_timeTable = QtGui.QGraphicsView(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_timeTable.sizePolicy().hasHeightForWidth())
        self.graphicsView_timeTable.setSizePolicy(sizePolicy)
        self.graphicsView_timeTable.setObjectName(_fromUtf8("graphicsView_timeTable"))
        self.horizontalLayout_2.addWidget(self.graphicsView_timeTable)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.gridLayout_2.addWidget(self.groupBox_event, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.buttonBox = QtGui.QDialogButtonBox(DienstplanForm)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_4.addWidget(self.buttonBox)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)

        self.retranslateUi(DienstplanForm)
        QtCore.QMetaObject.connectSlotsByName(DienstplanForm)

    def retranslateUi(self, DienstplanForm):
        DienstplanForm.setWindowTitle(_translate("DienstplanForm", "Dienstplan", None))
        self.label.setText(_translate("DienstplanForm", "Veranstaltung", None))
        self.pushButton_refresh.setText(_translate("DienstplanForm", "Aktualisieren", None))
        self.label_2.setText(_translate("DienstplanForm", "Voreinstellung", None))
        self.pushButton_loadTemplate.setText(_translate("DienstplanForm", "&Laden", None))
        self.pushButton_saveTemplate.setText(_translate("DienstplanForm", "&Speichern", None))
        self.pushButton_autoAssignEmps.setText(_translate("DienstplanForm", "DN autom. zuordnen", None))
        self.groupBox_event.setTitle(_translate("DienstplanForm", "Dienstplan", None))
        self.pushButton_addEmployee.setText(_translate("DienstplanForm", "&Hinzufügen", None))
        self.pushButton_sort.setText(_translate("DienstplanForm", "&Sortieren", None))

from lib.LMComboBox import LMComboBox
