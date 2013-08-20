# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection
import config

from forms.formBase import FormBase
from ui.forms.buchungskonten2artikelForm_gui import Ui_Buchungskonten2artikelForm

class Buchungskonten2artikelForm(FormBase):
	
	uiClass = Ui_Buchungskonten2artikelForm
	ident = 'buchungskonten2artikel'
	
	def setupUi(self):
		super(Buchungskonten2artikelForm, self).setupUi()
		
		m = self.model = QtSql.QSqlRelationalTableModel()
		m.setTable('buchungskonto2artikel')
		m.setRelation(m.fieldIndex('b2a_bukid'), QtSql.QSqlRelation('buchungskonten', 'buk_id', 'buk_bezeichnung'))
		m.setRelation(m.fieldIndex('b2a_artikel_id'), QtSql.QSqlRelation('artikel_basis', 'artikel_id', 'artikel_bezeichnung'))
		m.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		m.select()
		
		# column headers
		m.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
		m.setHeaderData(1, QtCore.Qt.Horizontal, 'Buchungskonto')
		m.setHeaderData(2, QtCore.Qt.Horizontal, 'Artikel')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView
		self.tableView.setModel(self.model)
		self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.setColumnHidden(m.fieldIndex('b2a_periode'), True)
		self.tableView.setColumnHidden(m.fieldIndex('b2a_id'), True)
		self.tableView.horizontalHeader().setStretchLastSection(True)
		
		self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)
		self.connect(self.ui.pushButton_initPeriod, QtCore.SIGNAL('clicked()'), self.initPeriod)
		
		self.model = m
		self.updateFilter()
		
	
	def newRecord(self):
		rec = self.model.record()
		rec.setValue(1, '')
		rec.setValue(2, '')
		rec.setValue(3, self.getCurrentPeriodId())
		self.model.insertRecord(-1, rec)
		
		
	def deleteRecord(self):
		selected = self.tableView.selectionModel().selectedRows(0);
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
	


	def initPeriod(self):
		query = QtSql.QSqlQuery()
		query.prepare('select count(*) from buchungskonto2artikel where b2a_periode = ?')
		query.addBindValue(self.getCurrentPeriodId())
		query.exec_()
		
		if query.lastError().isValid():
			print 'Error while getting buchungskonten 2 artikel relations for period:', query.lastError().text()
			QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
									'Periode konnte nicht initialisiert werden!\nBitte kontaktieren Sie Ihren Administrator.')
			return
		
		query.next()
		count = query.value(0).toInt()[0]
		
		if count > 0:
			QtGui.QMessageBox.warning(self, u'Periode bereits initialisiert', 
									u'Periode konnte nicht initialisiert werden, da bereits Zuordnungen für diese Periode vorhanden sind!')
			return
		
		
		self.beginTransaction()
		query = QtSql.QSqlQuery()
		query.prepare("""insert into buchungskonto2artikel (b2a_bukid, b2a_artikel_id, b2a_periode)
					select (select min(buk_id) from buchungskonten), lager_artikel_artikel, lager_artikel_periode from lager_artikel where lager_artikel_periode = ?""")
		query.addBindValue(self.getCurrentPeriodId())
		query.exec_()
		query.next()
		
		if query.lastError().isValid():
			self.rollback()
			print 'Error while setting initial buchungskonten 2 artikel relations for period:', query.lastError().text()
			QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
									'Periode konnte nicht initialisiert werden!\nBitte kontaktieren Sie Ihren Administrator.')
		else:
			self.commit()
			
		self.model.select()
		
		
	def updatePeriod(self, p):
		super(Buchungskonten2artikelForm, self).updatePeriod(p)
		self.updateFilter()
		
		
	def updateFilter(self):
		m = self.model
		relModel = m.relationModel(m.fieldIndex('artikel_bezeichnung'))
		relModel.setFilter('artikel_id in (select lager_artikel_artikel from lager_artikel where lager_artikel_periode = %(perId)s) and artikel_periode = %(perId)s'% {'perId':self.getCurrentPeriodId()})
		relModel.sort(1, QtCore.Qt.AscendingOrder)
	
		m.setFilter('b2a_periode = %(perId)s and artikel_periode = %(perId)s'% {'perId':self.getCurrentPeriodId()})
		m.select()