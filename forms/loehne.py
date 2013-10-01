# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection
import config
import lib.datetimehelper

from forms.formBase import FormBase
from ui.forms.loehneForm_gui import Ui_LoehneForm

class LoehneForm(FormBase):
	
	uiClass = Ui_LoehneForm
	ident = 'loehne'
	
	def setupUi(self):
		super(LoehneForm, self).setupUi()
		
		self.model = QtSql.QSqlRelationalTableModel()
		self.model.setTable('loehne')
		
		#the a record before setting the relations for use in the newRecord method
		self.baseRecord = self.model.record()
		
		self.model.setRelation(self.model.fieldIndex('loh_gehid'), QtSql.QSqlRelation('gehaelter', 'geh_id', 'geh_kbez'))
		
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()
		
		# column headers
		self.model.setHeaderData(0, QtCore.Qt.Horizontal, u'ID')
		self.model.setHeaderData(1, QtCore.Qt.Horizontal, u'Summe')
		self.model.setHeaderData(2, QtCore.Qt.Horizontal, u'Gehalt')
		self.model.setHeaderData(3, QtCore.Qt.Horizontal, u'gültig bis')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView
		self.tableView.setModel(self.model)
		self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.horizontalHeader().setStretchLastSection(True)
		self.tableView.setSortingEnabled(True)
		
		self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)
		
	
	def newRecord(self):
		rec = self.baseRecord
		rec.setValue(1, 0.0)
		self.model.insertRecord(-1, rec)
		
		
	def deleteRecord(self):
		selected = self.tableView.selectionModel().selectedRows(0);
		print selected
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
	
