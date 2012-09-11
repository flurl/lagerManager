# -*- coding: utf-8 -*-
import sys
import datetime

from PyQt4 import QtCore, QtGui, QtSql

from ui.lieferungenDlg_gui import Ui_LieferungenDialog

from CONSTANTS import *


class DateEditDelegate(QtGui.QItemDelegate):
	
	def createEditor(self, parent, option, index):
		editor = QtGui.QDateEdit()
		editor.setCalendarPopup(True)
		editor.setDate(datetime.datetime.now())
		return editor
		
class LagerartikelDelegate(QtGui.QItemDelegate):
	
	def createEditor(self, parent, option, index):
		editor = QtGui.QComboBox()
		return editor



class LieferungenDialog(QtGui.QDialog):
	
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)

		self.ui = Ui_LieferungenDialog()

		self.ui.setupUi(self)
		
		self._connectToDb()
		
		self._setupForm()
		
	
	
	def _setupForm(self):
	
		#Master table
		#------------------------------
		# column headers
		self.masterModel.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
		self.masterModel.setHeaderData(1, QtCore.Qt.Horizontal, 'Lieferant')
		self.masterModel.setHeaderData(2, QtCore.Qt.Horizontal, 'Datum')
		# table view
		self.masterTableView = self.ui.tableView_lieferungen
		self.masterTableView.setModel(self.masterModel)
		self.masterTableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.masterTableView))
		self.masterTableView.setItemDelegateForColumn(2, DateEditDelegate())
		self.masterTableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.masterTableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.masterTableView.resizeColumnsToContents()
		self.masterTableView.horizontalHeader().setStretchLastSection(True)
		
		
		#detail table
		#--------------------------------
		# column headers
		self.detailModel.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
		self.detailModel.setHeaderData(1, QtCore.Qt.Horizontal, 'Lieferung')
		self.detailModel.setHeaderData(2, QtCore.Qt.Horizontal, 'Artikel')
		self.detailModel.setHeaderData(3, QtCore.Qt.Horizontal, 'Anzahl')
		# table view
		# ------------------------------------------------
		self.detailTableView = self.ui.tableView_lieferungenDetails
		self.detailTableView.setModel(self.detailModel)
		self.detailTableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.detailTableView))
		self.detailTableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.detailTableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.detailTableView.resizeColumnsToContents()
		self.detailTableView.horizontalHeader().setStretchLastSection(True)
		
		self.connect(self.ui.pushButton_OK, QtCore.SIGNAL('clicked()'), self._onOKBtnClicked)
		self.connect(self.ui.pushButton_newLieferung, QtCore.SIGNAL('clicked()'), self._onNewLieferungBtnClicked)
		self.connect(self.ui.pushButton_deleteLieferung, QtCore.SIGNAL('clicked()'), self._onDeleteLieferungBtnClicked)
		self.connect(self.ui.pushButton_newDetail, QtCore.SIGNAL('clicked()'), self._onNewDetailBtnClicked)
		self.connect(self.ui.pushButton_deleteDetail, QtCore.SIGNAL('clicked()'), self._onDeleteDetailBtnClicked)
		self.connect(self.masterTableView.selectionModel(), QtCore.SIGNAL('selectionChanged(const QItemSelection&,const QItemSelection&)'), self._onMasterTableViewSelectionChanged)
		#self.connect(self.ui.comboBox_period, QtCore.SIGNAL('currentIndexChanged(int)'), self.setFilter)
		
		
		
	def _onOKBtnClicked(self):
		self.accept()
		
		
	
	def _onNewLieferungBtnClicked(self):
		query = "select min(lieferant_id) from lieferanten"
		results = self.db.exec_(query)
		results.next()
		lieferantId = results.value(0).toInt()[0]
		
		query = """insert into lieferungen (lieferant_id, datum) 
				values 
				(%s, '%s')""" % (lieferantId, datetime.datetime.now().strftime('%Y-%m-%d'))
	
		results = self.db.exec_(query)
		print self.db.lastError().text()
		self.db.commit()
		self.masterModel.select()
		
		
	def _onDeleteLieferungBtnClicked(self):
		selected = self.masterTableView.selectionModel().selectedRows()
		for i in range(len(selected)):
			self.masterModel.removeRows(selected[i].row(), 1)
		self.masterModel.submitAll()
	
	
	def _onNewDetailBtnClicked(self):
		lieferungId = self.getCurrentLieferungId()
		
		query = "select min(lager_artikel_artikel) from lager_artikel"
		results = self.db.exec_(query)
		results.next()
		artikelId = results.value(0).toInt()[0]
		
		query = """insert into lieferungen_details (lieferung_id, artikel_id, anzahl, einkaufspreis) 
				values 
				(%s, %s, %s, %s)""" % (lieferungId, artikelId, 1.0, 1.0)
		print query
		results = self.db.exec_(query)
		self.db.commit()
		self.detailModel.select()
		
		
	def _onDeleteDetailBtnClicked(self):
		selected = self.detailTableView.selectionModel().selectedRows()
		for i in range(len(selected)):
			self.detailModel.removeRows(selected[i].row(), 1)
		self.detailModel.submitAll()


	def _onMasterTableViewSelectionChanged(self, newSelection, oldSelection):
		self.updateDetailFilter()

			
			
			
	def _connectToDb(self):
		self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
		self.db.setHostName(DBHOST)
		self.db.setDatabaseName(DBNAME)
		self.db.setPassword(DBPASSWORD)
		self.db.setUserName(DBUSER)
		ok = self.db.open()  
		self.masterModel = QtSql.QSqlRelationalTableModel()
		self.masterModel.setTable('lieferungen')
		self.masterModel.setRelation(1, QtSql.QSqlRelation('lieferanten', 'lieferant_id', 'lieferant_name'))
		self.masterModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.masterModel.setSort(2, QtCore.Qt.AscendingOrder)
		self.masterModel.select()
		
		self.detailModel = QtSql.QSqlRelationalTableModel()
		self.detailModel.setTable('lieferungen_details')
		self.detailModel.setRelation(1, QtSql.QSqlRelation('lieferungen', 'lieferung_id', 'datum'))
		self.detailModel.setRelation(2, QtSql.QSqlRelation('artikel_basis', 'artikel_id', 'artikel_bezeichnung'))
		relModel = self.detailModel.relationModel(2)
		relModel.setFilter('artikel_id in (select lager_artikel_artikel from lager_artikel)')
		relModel.sort(1, QtCore.Qt.AscendingOrder)
		self.detailModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.detailModel.select()
		
			
			
	def getCurrentLieferungId(self):
		idx = self.masterTableView.selectionModel().currentIndex()
		id_, success = idx.sibling(idx.row(),0).data(QtCore.Qt.DisplayRole).toInt()
		if success:
			return id_
		else:
			return False
		
	def updateDetailFilter(self):
		self.detailModel.setFilter('lieferungen_details.lieferung_id=%s'%(self.getCurrentLieferungId(),))
		self.detailModel.select()
			
			
			
if __name__ == "__main__":
	SQLITEDB = 'WaWi.db'
	
	app = QtGui.QApplication(sys.argv)
	win = LieferungenDialog()
	win.show()
	sys.exit(app.exec_())
