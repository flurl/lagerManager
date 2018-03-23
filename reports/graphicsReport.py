from PyQt4 import QtCore

from reports.reportBase import ReportBase
from ui.reports.defaultGraphicsReport_gui import Ui_DefaultGraphicsReport

class GraphicsReport(ReportBase):
	uiClass = Ui_DefaultGraphicsReport
	
	def __init__(self, parent):
		ReportBase.__init__(self, parent)
		
		
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
		

