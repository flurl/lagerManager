# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection
import config

from forms.formBase import FormBase
from ui.forms.dienstnehmerForm_gui import Ui_DienstnehmerForm
from lib.ColorDialogDelegate import ColorDialogDelegate

class DienstnehmerForm(FormBase):
	
	uiClass = Ui_DienstnehmerForm
	ident = 'dienstnehmer'
	
	def setupUi(self):
		super(DienstnehmerForm, self).setupUi()
		
		self.model = QtSql.QSqlRelationalTableModel()
		self.model.setTable('dienstnehmer')
		self.model.setRelation(self.model.fieldIndex('din_bebid'), QtSql.QSqlRelation('beschaeftigungsbereiche', 'beb_id', 'beb_bezeichnung'))
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.setSort(self.model.fieldIndex('din_id'), QtCore.Qt.AscendingOrder)
		self.model.select()
		
		# column headers
		self.model.setHeaderData(0, QtCore.Qt.Horizontal, u'ID')
		self.model.setHeaderData(1, QtCore.Qt.Horizontal, u'Name')
		self.model.setHeaderData(2, QtCore.Qt.Horizontal, u'Gehalt')
		self.model.setHeaderData(3, QtCore.Qt.Horizontal, u'Beschäftigungsbereich')
		self.model.setHeaderData(4, QtCore.Qt.Horizontal, u'Stundenlohn')
		self.model.setHeaderData(5, QtCore.Qt.Horizontal, u'Farbe')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView_dienstnehmer
		self.tableView.setModel(self.model)
		self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.horizontalHeader().setStretchLastSection(True)
		self.tableView.setSortingEnabled(True)
		
		delegate = ColorDialogDelegate()
		delegate.setColorColumn(5)
		#self.connect(delegate, QtCore.SIGNAL('colorColumnEdit(const QModelIndex&)', self.openColorDialog)
		self.tableView.setItemDelegate(delegate)
		
		self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)
		
	
	def newRecord(self):
		query = QtSql.QSqlQuery()
		query.prepare("""select min(beb_id) from beschaeftigungsbereiche""")
		query.exec_()
		query.next()
		minBebId = query.value(0).toInt()[0]
		
		rec = self.model.record()
		rec.setValue(1, '')
		rec.setValue(2, 0.0)
		rec.setValue(self.model.fieldIndex('beb_bezeichnung'), QtCore.QVariant(minBebId))
		rec.setValue(self.model.fieldIndex('din_stundensatz'), 0.0)
		#self.model.insertRecord(-1, rec)
		self.model.insertRowIntoTable(rec)
		self.model.select()
		
		
	def deleteRecord(self):
		selected = self.tableView.selectionModel().selectedRows(0);
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
		
	
