# -*- coding: utf-8 -*-
import decimal
import sys

from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *

from ui.lagerstandDlg_gui import Ui_LagerstandDialog

class LagerstandDialog(QtGui.QDialog):
	
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)

		self.ui = Ui_LagerstandDialog()

		self.ui.setupUi(self)
		
		self._connectToDb()
		
		self._setupForm()
		
	
	
	def _setupForm(self):
	
		query = "select periode_id, periode_bezeichnung from perioden order by periode_id desc"
	
		results = self.db.exec_(query)
		
		while results.next():
			id_ = results.value(0).toInt()[0]
			name = results.value(1).toString()
			self.ui.comboBox_period.addItem(name, QtCore.QVariant(int(id_)))

		self.setFilter()
	
		# column headers
		self.model.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
		self.model.setHeaderData(1, QtCore.Qt.Horizontal, 'Artikel')
		self.model.setHeaderData(2, QtCore.Qt.Horizontal, 'Anzahl')
		self.model.setHeaderData(3, QtCore.Qt.Horizontal, 'Periode')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView_lagerstand
		self.tableView.setModel(self.model)
		self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.horizontalHeader().setStretchLastSection(True)
		
		self.connect(self.ui.pushButton_OK, QtCore.SIGNAL('clicked()'), self._onOKBtnClicked)
		self.connect(self.ui.pushButton_initPeriod, QtCore.SIGNAL('clicked()'), self._onInitPeriodBtnClicked)
		self.connect(self.ui.comboBox_period, QtCore.SIGNAL('currentIndexChanged(int)'), self.setFilter)
		
		
		
	def _onOKBtnClicked(self):
		self.accept()
		
		
	"""
	def _onNewRecordBtnClicked(self):
		rec = self.model.record()
		rec.setValue(1, '')
		self.model.insertRecord(-1, rec)
		
		
	def _onDeleteRecordBtnClicked(self):
		selected = self.tableView.selectionModel().selectedIndexes();
		for i in range(len(selected)-1):
			print 'deleting'
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
	"""
	
	def _onInitPeriodBtnClicked(self):
		query = """insert into lagerstand (artikel_id, anzahl, periode_id)
					select lager_artikel_artikel, 0, lager_artikel_periode from lager_artikel where lager_artikel_periode = %s""" % (self._getCurrentPeriodId(), )
		print query
		results = self.db.exec_(query)
		
		self.db.commit()
			
			
			
	def _connectToDb(self):
		self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
		self.db.setHostName(DBHOST)
		self.db.setDatabaseName(DBNAME)
		self.db.setPassword(DBPASSWORD)
		self.db.setUserName(DBUSER)
		ok = self.db.open()  
		self.model = QtSql.QSqlRelationalTableModel()
		self.model.setTable('lagerstand')
		self.model.setRelation(1, QtSql.QSqlRelation('artikel_basis', 'artikel_id', 'artikel_bezeichnung'))
		self.model.setRelation(3, QtSql.QSqlRelation('perioden', 'periode_id', 'periode_bezeichnung'))
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()
		#print self.model.select()
		
		
		
	def _getCurrentPeriodId(self):
		return self.ui.comboBox_period.itemData(self.ui.comboBox_period.currentIndex()).toInt()[0]
			
			
	def setFilter(self):
		print "filter", 'periode_id=%s'%(self._getCurrentPeriodId(),)
		self.model.setFilter('lagerstand.periode_id=%s'%(self._getCurrentPeriodId(),))
		self.model.select()
			
			
if __name__ == "__main__":
	SQLITEDB = 'WaWi.db'
	
	app = QtGui.QApplication(sys.argv)
	win = LagerstandDialog()
	win.show()
	sys.exit(app.exec_())
