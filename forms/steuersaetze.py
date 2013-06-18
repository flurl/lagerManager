# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection
import config

from forms.formBase import FormBase
from ui.forms.steuersaetzeForm_gui import Ui_SteuersaetzeForm

class SteuersaetzeForm(FormBase):
	
	uiClass = Ui_SteuersaetzeForm
	ident = 'steuersaetze'
	
	def setupUi(self):
		super(SteuersaetzeForm, self).setupUi()
		
		self.model = QtSql.QSqlTableModel()
		self.model.setTable('steuersaetze')
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()
		
		# column headers
		self.model.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
		self.model.setHeaderData(1, QtCore.Qt.Horizontal, 'Bezeichnung')
		self.model.setHeaderData(2, QtCore.Qt.Horizontal, 'Prozent')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView_steuersaetze
		self.tableView.setModel(self.model)
		self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.horizontalHeader().setStretchLastSection(True)
		
		self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)
		
	
	def newRecord(self):
		rec = self.model.record()
		rec.setValue(1, '')
		self.model.insertRecord(-1, rec)
		
		
	def deleteRecord(self):
		selected = self.tableView.selectionModel().selectedRows();
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
	
