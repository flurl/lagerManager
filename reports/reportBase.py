from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
from DBConnection import dbConn

class ReportBase(QtGui.QWidget):
	
	def __init__(self, parent):
		QtGui.QWidget.__init__(self, parent)
		
		self.currentPeriod = 0
		
		self.connectToDb()
		self.setupUi()
		self.setupSignals()
		
	
	def setupUi(self):
		self.ui = self.uiClass()
		self.ui.setupUi(self)
		self.populatePeriodCB()
		
		
	def setupSignals(self):
		#self.populatePeriodCB()
		self.connect(self.ui.comboBox_period, QtCore.SIGNAL('currentIndexChanged(int)'), lambda: self.updatePeriod(self._getCurrentPeriodId()))

		
	def connectToDb(self):
		self.db = dbConn
			
			
	def populatePeriodCB(self):
		query = "select periode_id, periode_bezeichnung from perioden order by periode_bezeichnung desc"
		results = self.db.exec_(query)
	
		while results.next():
			id_ = results.value(0).toInt()[0]
			name = results.value(1).toString()
			self.ui.comboBox_period.addItem(name, QtCore.QVariant(int(id_)))
			
	def _getCurrentPeriodId(self):
		return self.ui.comboBox_period.itemData(self.ui.comboBox_period.currentIndex()).toInt()[0]
	
	def _getCurrentPeriodStartEnd(self):
		query = QtSql.QSqlQuery()
		
		query.prepare("select periode_start, periode_ende from perioden where periode_id = ?")
		query.bindValue(0, self._getCurrentPeriodId())
		
		query.exec_()
	
		query.next()
		start = query.value(0).toDate().toPyDate()
		end = query.value(1).toDate().toPyDate()
			
		return start, end
	
			
	def updatePeriod(self, p):
		print 'ReportBase:updatePeriod', p
		self.currentPeriod = p
		self.updateData()
		
		
	def closeEvent(self, event):
		parent = self.parent()
		while parent:
			if isinstance(parent, QtGui.QMainWindow):
				parent.deregisterWindow(self)
				break
			else:
				parent = parent.parent()
				
		super(ReportBase, self).closeEvent(event)
