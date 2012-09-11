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
		
	def plot(self):
		self.ui.graphicsView.plot()
		
	def setDataFormatter(self, f=None):
		self.ui.graphicsView.setDataFormatter(f)
		

