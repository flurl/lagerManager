# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reports/reportGraphicsView.ui'
#
# Created: Wed Nov 21 20:56:18 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ReportGraphicsView(object):
    def setupUi(self, ReportGraphicsView):
        ReportGraphicsView.setObjectName("ReportGraphicsView")
        ReportGraphicsView.resize(823, 622)
        self.gridLayout = QtGui.QGridLayout(ReportGraphicsView)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_zoomIn = QtGui.QPushButton(ReportGraphicsView)
        self.pushButton_zoomIn.setObjectName("pushButton_zoomIn")
        self.horizontalLayout.addWidget(self.pushButton_zoomIn)
        self.pushButton_zoomOut = QtGui.QPushButton(ReportGraphicsView)
        self.pushButton_zoomOut.setObjectName("pushButton_zoomOut")
        self.horizontalLayout.addWidget(self.pushButton_zoomOut)
        self.checkBox_highlightNegative = QtGui.QCheckBox(ReportGraphicsView)
        self.checkBox_highlightNegative.setChecked(True)
        self.checkBox_highlightNegative.setObjectName("checkBox_highlightNegative")
        self.horizontalLayout.addWidget(self.checkBox_highlightNegative)
        self.slider_minDP = QtGui.QSlider(ReportGraphicsView)
        self.slider_minDP.setOrientation(QtCore.Qt.Horizontal)
        self.slider_minDP.setObjectName("slider_minDP")
        self.horizontalLayout.addWidget(self.slider_minDP)
        self.spinBox_minDP = QtGui.QSpinBox(ReportGraphicsView)
        self.spinBox_minDP.setObjectName("spinBox_minDP")
        self.horizontalLayout.addWidget(self.spinBox_minDP)
        self.slider_maxDP = QtGui.QSlider(ReportGraphicsView)
        self.slider_maxDP.setOrientation(QtCore.Qt.Horizontal)
        self.slider_maxDP.setObjectName("slider_maxDP")
        self.horizontalLayout.addWidget(self.slider_maxDP)
        self.spinBox_maxDP = QtGui.QSpinBox(ReportGraphicsView)
        self.spinBox_maxDP.setObjectName("spinBox_maxDP")
        self.horizontalLayout.addWidget(self.spinBox_maxDP)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.graphicsView = QtGui.QGraphicsView(ReportGraphicsView)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(ReportGraphicsView)
        QtCore.QObject.connect(self.slider_maxDP, QtCore.SIGNAL("valueChanged(int)"), self.spinBox_maxDP.setValue)
        QtCore.QObject.connect(self.slider_minDP, QtCore.SIGNAL("valueChanged(int)"), self.spinBox_minDP.setValue)
        QtCore.QObject.connect(self.spinBox_maxDP, QtCore.SIGNAL("valueChanged(int)"), self.slider_maxDP.setValue)
        QtCore.QObject.connect(self.spinBox_minDP, QtCore.SIGNAL("valueChanged(int)"), self.slider_minDP.setValue)
        QtCore.QMetaObject.connectSlotsByName(ReportGraphicsView)

    def retranslateUi(self, ReportGraphicsView):
        ReportGraphicsView.setWindowTitle(QtGui.QApplication.translate("ReportGraphicsView", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_zoomIn.setText(QtGui.QApplication.translate("ReportGraphicsView", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_zoomOut.setText(QtGui.QApplication.translate("ReportGraphicsView", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_highlightNegative.setText(QtGui.QApplication.translate("ReportGraphicsView", "Negative Werte hervorheben", None, QtGui.QApplication.UnicodeUTF8))

