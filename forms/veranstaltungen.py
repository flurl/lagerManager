# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection
import config

from forms.formBase import FormBase
from ui.forms.veranstaltungenForm_gui import Ui_VeranstaltungenForm

import datetime

class VeranstaltungenForm(FormBase):
	
	uiClass = Ui_VeranstaltungenForm
	ident = 'veranstaltungen'
	
	def setupUi(self):
		super(VeranstaltungenForm, self).setupUi()
		
		self.model = QtSql.QSqlRelationalTableModel()
		self.model.setJoinMode(QtSql.QSqlRelationalTableModel.LeftJoin)
		self.model.setTable('veranstaltungen')
		self.model.setRelation(self.model.fieldIndex('ver_checkpointid'), QtSql.QSqlRelation('journal_checkpoints', 'checkpoint_id', 'checkpoint_info'))
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()

		
		# column headers
		self.model.setHeaderData(0, QtCore.Qt.Horizontal, u'ID')
		self.model.setHeaderData(1, QtCore.Qt.Horizontal, u'Datum')
		self.model.setHeaderData(2, QtCore.Qt.Horizontal, u'Bezeichnung')
		self.model.setHeaderData(3, QtCore.Qt.Horizontal, u'Beginn')
		self.model.setHeaderData(4, QtCore.Qt.Horizontal, u'Checkpoint')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView_veranstaltungen
		self.tableView.setModel(self.model)
		self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.horizontalHeader().setStretchLastSection(True)
		self.tableView.setSortingEnabled(True)
		self.tableView.sortByColumn(self.model.fieldIndex('ver_datum'), QtCore.Qt.DescendingOrder)
		
		self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)
		
		
	def setupSignals(self):
		super(VeranstaltungenForm, self).setupSignals()
		
		self.connect(self.ui.pushButton_autoCreate, QtCore.SIGNAL('clicked()'), self.openAutoCreateForm)
		
	
	def newRecord(self):
		rec = self.model.record()
		rec.setValue(1, QtCore.QVariant(QtCore.QDate.currentDate()))
		rec.setValue(2, '')
		rec.setValue(3, QtCore.QVariant(QtCore.QTime.currentTime()))
		
		#self.model.insertRecord(-1, rec)
		self.model.insertRowIntoTable(rec)
		self.model.select()
		
		
	def deleteRecord(self):
		selected = self.tableView.selectionModel().selectedRows(0);
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
		
		
	def openAutoCreateForm(self):
		import forms.autoCreateShifts
		form = forms.autoCreateShifts.AutoCreateShiftsForm(self)
		form.show()
		
	
