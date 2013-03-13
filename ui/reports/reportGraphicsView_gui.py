# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/reportGraphicsView.ui'
#
# Created: Wed Mar 13 15:46:48 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ReportGraphicsView(object):
    def setupUi(self, ReportGraphicsView):
        ReportGraphicsView.setObjectName(_fromUtf8("ReportGraphicsView"))
        ReportGraphicsView.resize(823, 622)
        self.gridLayout = QtGui.QGridLayout(ReportGraphicsView)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_zoomIn = QtGui.QPushButton(ReportGraphicsView)
        self.pushButton_zoomIn.setObjectName(_fromUtf8("pushButton_zoomIn"))
        self.horizontalLayout.addWidget(self.pushButton_zoomIn)
        self.pushButton_zoomOut = QtGui.QPushButton(ReportGraphicsView)
        self.pushButton_zoomOut.setObjectName(_fromUtf8("pushButton_zoomOut"))
        self.horizontalLayout.addWidget(self.pushButton_zoomOut)
        self.checkBox_highlightNegative = QtGui.QCheckBox(ReportGraphicsView)
        self.checkBox_highlightNegative.setChecked(True)
        self.checkBox_highlightNegative.setObjectName(_fromUtf8("checkBox_highlightNegative"))
        self.horizontalLayout.addWidget(self.checkBox_highlightNegative)
        self.checkBox_showMarkings = QtGui.QCheckBox(ReportGraphicsView)
        self.checkBox_showMarkings.setChecked(True)
        self.checkBox_showMarkings.setObjectName(_fromUtf8("checkBox_showMarkings"))
        self.horizontalLayout.addWidget(self.checkBox_showMarkings)
        self.slider_minDP = QtGui.QSlider(ReportGraphicsView)
        self.slider_minDP.setOrientation(QtCore.Qt.Horizontal)
        self.slider_minDP.setObjectName(_fromUtf8("slider_minDP"))
        self.horizontalLayout.addWidget(self.slider_minDP)
        self.spinBox_minDP = QtGui.QSpinBox(ReportGraphicsView)
        self.spinBox_minDP.setObjectName(_fromUtf8("spinBox_minDP"))
        self.horizontalLayout.addWidget(self.spinBox_minDP)
        self.slider_maxDP = QtGui.QSlider(ReportGraphicsView)
        self.slider_maxDP.setOrientation(QtCore.Qt.Horizontal)
        self.slider_maxDP.setObjectName(_fromUtf8("slider_maxDP"))
        self.horizontalLayout.addWidget(self.slider_maxDP)
        self.spinBox_maxDP = QtGui.QSpinBox(ReportGraphicsView)
        self.spinBox_maxDP.setObjectName(_fromUtf8("spinBox_maxDP"))
        self.horizontalLayout.addWidget(self.spinBox_maxDP)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.graphicsView = QtGui.QGraphicsView(ReportGraphicsView)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout.addWidget(self.graphicsView)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(ReportGraphicsView)
        QtCore.QObject.connect(self.slider_maxDP, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spinBox_maxDP.setValue)
        QtCore.QObject.connect(self.slider_minDP, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spinBox_minDP.setValue)
        QtCore.QObject.connect(self.spinBox_maxDP, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.slider_maxDP.setValue)
        QtCore.QObject.connect(self.spinBox_minDP, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.slider_minDP.setValue)
        QtCore.QMetaObject.connectSlotsByName(ReportGraphicsView)

    def retranslateUi(self, ReportGraphicsView):
        ReportGraphicsView.setWindowTitle(QtGui.QApplication.translate("ReportGraphicsView", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_zoomIn.setText(QtGui.QApplication.translate("ReportGraphicsView", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_zoomOut.setText(QtGui.QApplication.translate("ReportGraphicsView", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_highlightNegative.setText(QtGui.QApplication.translate("ReportGraphicsView", "Negative markieren", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_showMarkings.setText(QtGui.QApplication.translate("ReportGraphicsView", "Beschriftung anzeigen", None, QtGui.QApplication.UnicodeUTF8))

