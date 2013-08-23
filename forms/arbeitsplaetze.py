# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection
import config

from forms.formBase import FormBase
from ui.forms.arbeitsplaetzeForm_gui import Ui_ArbeitsplaetzeForm

class ArbeitsplaetzeForm(FormBase):
	
	uiClass = Ui_ArbeitsplaetzeForm
	ident = 'arbeitsplaetze'
	
	def setupUi(self):
		super(ArbeitsplaetzeForm, self).setupUi()
		
		self.model = QtSql.QSqlRelationalTableModel()
		self.model.setTable('arbeitsplaetze')
		
		#the a record before setting the relations for use in the newRecord method
		self.baseRecord = self.model.record()
		
		self.model.setRelation(self.model.fieldIndex('arp_bebid'), QtSql.QSqlRelation('beschaeftigungsbereiche', 'beb_id', 'beb_bezeichnung'))
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()
		
		# column headers
		self.model.setHeaderData(0, QtCore.Qt.Horizontal, u'ID')
		self.model.setHeaderData(1, QtCore.Qt.Horizontal, u'Bezeichnung')
		self.model.setHeaderData(2, QtCore.Qt.Horizontal, u'Standard Dienst Dauer')
		self.model.setHeaderData(3, QtCore.Qt.Horizontal, u'Beschäftigungsbereich')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView_arbeitsplaetze
		self.tableView.setModel(self.model)
		self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.horizontalHeader().setStretchLastSection(True)
		
		self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)
		
	
	def newRecord(self):
		query = QtSql.QSqlQuery()
		query.prepare("""select min(beb_id) from beschaeftigungsbereiche""")
		query.exec_()
		query.next()
		minBebId = query.value(0).toInt()[0]

		rec = self.baseRecord
		rec.setValue(1, '')
		rec.setValue(2, 0.0)
		rec.setValue(3, minBebId)
		self.model.insertRecord(-1, rec)
		
		
	def deleteRecord(self):
		selected = self.tableView.selectionModel().selectedRows(0);
		print selected
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
	
