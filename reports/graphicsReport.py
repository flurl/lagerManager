from PyQt4 import QtCore, QtGui

from lib.UnicodeWriter import UnicodeWriter

from reports.reportBase import ReportBase
from ui.reports.defaultGraphicsReport_gui import Ui_DefaultGraphicsReport

class GraphicsReport(ReportBase):
	uiClass = Ui_DefaultGraphicsReport
	
	def __init__(self, parent):
		ReportBase.__init__(self, parent)
		
	def setupSignals(self):
		ReportBase.setupSignals(self)
		if self.ui.pushButton_export:
			self.connect(self.ui.pushButton_export, QtCore.SIGNAL('clicked()'),
						self.exportData)
		
	def setDatapoints(self, dp):
		print "GV setDatapoints"
		self.dataPoints = dp
		self.ui.graphicsView.setDatapoints(dp)
		
	def setExtraData(self, extraData=None):
		self.ui.graphicsView.setExtraData(extraData)
		
	def setMarkingData(self, markingData=[]):
		self.ui.graphicsView.setMarkingData(markingData)
		
	def plot(self):
		self.ui.graphicsView.plot()
		
	def setDataFormatter(self, f=None):
		self.ui.graphicsView.setDataFormatter(f)
		
	def getColor(self, key):
		return self.ui.graphicsView.getColor(key)
		
	def getCurrPeriode(self):
		return self.ui.comboBox_period.currentText()
		
	def exportData(self):
		l = []
		for k, v in self.dataPoints.items():
			l2 = [k]
			for k2, v2 in v.items():
				l2.extend([k2, v2])
			l.append(l2)
		
		filename = QtGui.QFileDialog.getSaveFileName(self, 'Datei speichern',
														'', 'CSV Files (*.csv)')
		with open(filename, 'wb') as f:
			writer = UnicodeWriter(f)
			writer.writerows(l)

