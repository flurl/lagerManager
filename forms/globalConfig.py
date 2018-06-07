# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection

from forms.formBase import FormBase
from ui.forms.configForm_gui import Ui_ConfigForm


class ConfigForm(FormBase):
	
	uiClass = Ui_ConfigForm
	ident = 'config'
	
	def setupUi(self):
		super(ConfigForm, self).setupUi()
		
		self.model = QtSql.QSqlTableModel()
		self.model.setTable('config')
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()

		
		# column headers
		self.model.setHeaderData(0, QtCore.Qt.Horizontal, u'ID')
		self.model.setHeaderData(1, QtCore.Qt.Horizontal, u'Key')
		self.model.setHeaderData(2, QtCore.Qt.Horizontal, u'ValueI')
		self.model.setHeaderData(3, QtCore.Qt.Horizontal, u'ValueF')
		self.model.setHeaderData(4, QtCore.Qt.Horizontal, u'ValueS')
		self.model.setHeaderData(5, QtCore.Qt.Horizontal, u'gültig bis')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView
		self.tableView.setModel(self.model)
		#self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.horizontalHeader().setStretchLastSection(True)
		
		self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)
		
	
	def newRecord(self):
		rec = self.model.record()
		rec.setValue(1, '')
		rec.setValue(2, QtCore.QVariant())
		rec.setValue(3, QtCore.QVariant())
		rec.setValue(4, QtCore.QVariant())
		rec.setValue(5, QtCore.QVariant())
		
		self.model.insertRecord(-1, rec)
		#self.model.insertRowIntoTable(rec)
		#self.model.select()
		
		
	def deleteRecord(self):
		selected = self.tableView.selectionModel().selectedRows(0);
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
	
