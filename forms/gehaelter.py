# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection
import config
import lib.datetimehelper

from forms.formBase import FormBase
from ui.forms.gehaelterForm_gui import Ui_GehaelterForm

class GehaelterForm(FormBase):
	
	uiClass = Ui_GehaelterForm
	ident = 'gehaelter'
	
	def setupUi(self):
		super(GehaelterForm, self).setupUi()
		
		self.model = QtSql.QSqlTableModel()
		self.model.setTable('gehaelter')
		
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()
		
		# column headers
		self.model.setHeaderData(0, QtCore.Qt.Horizontal, u'ID')
		self.model.setHeaderData(1, QtCore.Qt.Horizontal, u'Kurzbezeichnung')
		self.model.setHeaderData(2, QtCore.Qt.Horizontal, u'Bezeichnung')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView
		self.tableView.setModel(self.model)
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.horizontalHeader().setStretchLastSection(True)
		self.tableView.setSortingEnabled(True)
		
		self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)
		
	
	def newRecord(self):
		rec = self.model.record()
		rec.setValue(1, '')
		rec.setValue(2, '')
		self.model.insertRecord(-1, rec)
		
		
	def deleteRecord(self):
		selected = self.tableView.selectionModel().selectedRows(0);
		print selected
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
	
