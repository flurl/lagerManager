# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection
import config

from forms.formBase import FormBase
from ui.forms.dirTypenForm_gui import Ui_DirTypenForm
from lib.LineEditDelegate import LineEditDelegate

class DirTypenForm(FormBase):
	
	uiClass = Ui_DirTypenForm
	ident = 'dir_typen'
	
	def setupUi(self):
		super(DirTypenForm, self).setupUi()
		
		self.model = QtSql.QSqlTableModel()
		self.model.setTable('dir_typen')
		
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()
		
		#self.model.setRelation(self.model.fieldIndex('dit_beginn_ditid'), QtSql.QSqlRelation('dir_typen', 'dit_id', 'dit_kbez'))
		#self.model.setRelation(self.model.fieldIndex('dit_ende_ditid'), QtSql.QSqlRelation('dir_typen', 'dit_id', 'dit_kbez'))
		
		# column headers
		self.model.setHeaderData(self.model.fieldIndex('dit_id'), QtCore.Qt.Horizontal, u'ID')
		self.model.setHeaderData(self.model.fieldIndex('dit_bez'), QtCore.Qt.Horizontal, u'Bezeichnung')
		self.model.setHeaderData(self.model.fieldIndex('dit_kbez'), QtCore.Qt.Horizontal, u'Kurzbezeichnung')
		self.model.setHeaderData(self.model.fieldIndex('dit_beginn_ditid'), QtCore.Qt.Horizontal, u'Beginn Typ')
		self.model.setHeaderData(self.model.fieldIndex('dit_ende_ditid'), QtCore.Qt.Horizontal, u'Ende Typ')
		
		

		
		# table view
		# ------------------------------------------------
		delegate = LineEditDelegate(True)
		self.tableView = self.ui.tableView
		self.tableView.setItemDelegateForColumn(self.model.fieldIndex('dit_beginn_ditid'), delegate)
		self.tableView.setItemDelegateForColumn(self.model.fieldIndex('dit_ende_ditid'), delegate)
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
		rec.setValue(self.model.fieldIndex('dit_bez'), '')
		rec.setValue(self.model.fieldIndex('dit_kbez'), '')
		self.model.insertRecord(-1, rec)
		
		
	def deleteRecord(self):
		selected = self.tableView.selectionModel().selectedRows(0);
		print selected
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
	
