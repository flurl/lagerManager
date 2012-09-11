from PyQt4 import QtCore, QtGui

from CONSTANTS import *

from ui.reports.reportTextView_gui import Ui_ReportTextView


class ReportTextViewWidget(QtGui.QWidget):
	
	def __init__(self, parent):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_ReportTextView()
		self.ui.setupUi(self)
		
	def setText(self, text):
		self.ui.textEdit.setText(text)
