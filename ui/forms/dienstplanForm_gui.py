# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/forms/dienstplanForm.ui'
#
# Created: Sat Oct 12 01:16:47 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DienstplanForm(object):
    def setupUi(self, DienstplanForm):
        DienstplanForm.setObjectName(_fromUtf8("DienstplanForm"))
        DienstplanForm.resize(1176, 729)
        self.verticalLayout = QtGui.QVBoxLayout(DienstplanForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
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
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        self.verticalLayout.addLayout(self.horizontalLayout_3)
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1132, 555))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_employees = QtGui.QVBoxLayout()
        self.verticalLayout_employees.setObjectName(_fromUtf8("verticalLayout_employees"))
        self.pushButton_addEmployee = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_addEmployee.setObjectName(_fromUtf8("pushButton_addEmployee"))
        self.verticalLayout_employees.addWidget(self.pushButton_addEmployee)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_employees.addItem(spacerItem2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_employees)
        self.graphicsView_timeTable = QtGui.QGraphicsView(self.scrollAreaWidgetContents)
        self.graphicsView_timeTable.setObjectName(_fromUtf8("graphicsView_timeTable"))
        self.horizontalLayout_2.addWidget(self.graphicsView_timeTable)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.groupBox_event)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.buttonBox = QtGui.QDialogButtonBox(DienstplanForm)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_4.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(DienstplanForm)
        QtCore.QMetaObject.connectSlotsByName(DienstplanForm)

    def retranslateUi(self, DienstplanForm):
        DienstplanForm.setWindowTitle(QtGui.QApplication.translate("DienstplanForm", "Dienstplan", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DienstplanForm", "Veranstaltung", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_refresh.setText(QtGui.QApplication.translate("DienstplanForm", "Aktualisieren", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DienstplanForm", "Voreinstellung", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_loadTemplate.setText(QtGui.QApplication.translate("DienstplanForm", "&Laden", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_saveTemplate.setText(QtGui.QApplication.translate("DienstplanForm", "&Speichern", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_autoAssignEmps.setText(QtGui.QApplication.translate("DienstplanForm", "DN autom. zuordnen", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_event.setTitle(QtGui.QApplication.translate("DienstplanForm", "GroupBox", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_addEmployee.setText(QtGui.QApplication.translate("DienstplanForm", "&Hinzufügen", None, QtGui.QApplication.UnicodeUTF8))

from lib.LMComboBox import LMComboBox
