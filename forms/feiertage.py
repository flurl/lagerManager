# -*- coding: utf-8 -*-
import decimal
import sys
import csv
import datetime

from PyQt4 import QtCore, QtGui, QtSql

#from lib.UnicodeWriter import UnicodeWriter
from forms.formBase import FormBase
from ui.forms.feiertageForm_gui import Ui_FeiertageForm
import config


class FeiertageForm(FormBase):
	
	uiClass = Ui_FeiertageForm
	ident = 'feiertage'
	
	
	def setupUi(self):
		super(FeiertageForm, self).setupUi()
	
		self.model = QtSql.QSqlRelationalTableModel()
		self.model.setTable('feiertage')
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()
	
		# column headers
		self.model.setHeaderData(self.model.fieldIndex('fta_id'), QtCore.Qt.Horizontal, 'ID')
		self.model.setHeaderData(self.model.fieldIndex('fta_datum'), QtCore.Qt.Horizontal, 'Datum')
		self.model.setHeaderData(self.model.fieldIndex('fta_bezeichnung'), QtCore.Qt.Horizontal, 'Bezeichnung')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView
		self.tableView.setModel(self.model)
		self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.horizontalHeader().setStretchLastSection(True)
		
		
		
	def setupSignals(self):
		self.connect(self.ui.comboBox_period, QtCore.SIGNAL('currentIndexChanged(int)'), lambda: self.setFilter())

		super(FeiertageForm, self).setupSignals()

		self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)

	def setFilter(self):
		pass
		#self.model.setFilter('year(fta_datum)="%(periodYear)s" '%{'periodYear':self.ui.comboBox_period.currentText()})
		#self.model.select()


	def newRecord(self):
		rec = self.model.record()
		rec.setValue(self.model.fieldIndex('fta_datum'), datetime.datetime.now())
		rec.setValue(self.model.fieldIndex('fta_bezeichnung'), '')
		#self.model.insertRecord(-1, rec)
		self.model.insertRowIntoTable(rec)
		self.model.select()
		self.tableView.scrollToBottom()
		
		
	def deleteRecord(self):
		selected = self.tableView.selectionModel().selectedRows(0);
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
		

