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
		self.model.setRelation(self.model.fieldIndex('din_gehid'), QtSql.QSqlRelation('gehaelter', 'geh_id', 'geh_kbez'))
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.setSort(self.model.fieldIndex('din_id'), QtCore.Qt.AscendingOrder)
		self.model.select()
		
		# column headers
		self.model.setHeaderData(self.model.fieldIndex('din_id'), QtCore.Qt.Horizontal, u'ID')
		self.model.setHeaderData(self.model.fieldIndex('din_name'), QtCore.Qt.Horizontal, u'Name')
		self.model.setHeaderData(self.model.fieldIndex('din_gehalt'), QtCore.Qt.Horizontal, u'Max. Lohn')
		self.model.setHeaderData(self.model.fieldIndex('beb_bezeichnung'), QtCore.Qt.Horizontal, u'Beschäftigungsbereich')
		self.model.setHeaderData(self.model.fieldIndex('geh_kbez'), QtCore.Qt.Horizontal, u'Gehalt')
		self.model.setHeaderData(self.model.fieldIndex('din_farbe'), QtCore.Qt.Horizontal, u'Farbe')
		self.model.setHeaderData(self.model.fieldIndex('din_nummer'), QtCore.Qt.Horizontal, u'Nummer')
		

		
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
		
		delegate = ColorDialogDelegate(self.tableView)
		delegate.setColorColumn(self.model.fieldIndex('din_farbe'))
		#self.connect(delegate, QtCore.SIGNAL('colorColumnEdit(const QModelIndex&)', self.openColorDialog)
		self.tableView.setItemDelegate(delegate)
		
		fromIndex = self.model.fieldIndex('din_nummer')
		toIndex   = 1
		if fromIndex != toIndex: 
				self.tableView.horizontalHeader().moveSection(fromIndex, toIndex)
		
		self.createContextMenu()
		
		self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)
		
	
	def createContextMenu(self):
	
		#employee incident types context menu
		query = QtSql.QSqlQuery()
		query.prepare('select dit_id, dit_kbez from dir_typen')
		query.exec_()
		if query.lastError().isValid():
			print 'Error selecting emp incident types for context menu:', query.lastError().text()
		else:
			actions = []
			while query.next():
				ditId = query.value(0).toInt()[0]
				bez = query.value(1).toString()
				actions.append(QtGui.QAction(bez, self))
				self.connect(actions[-1], QtCore.SIGNAL('triggered()'), lambda dId=ditId: self.createNewEmpIncident(dId))
				self.ui.tableView_dienstnehmer.addAction(actions[-1])
				
		self.ui.tableView_dienstnehmer.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
	
	
	def createNewEmpIncident(self, ditId):
		idxList = self.ui.tableView_dienstnehmer.selectedIndexes()
		idx = idxList[0]
		idx = idx.sibling(idx.row(), 0)
		empId = self.model.data(idx)
		
		import forms.dienstnehmerEreignisse
		form = forms.dienstnehmerEreignisse.DienstnehmerEreignisseForm(self)
		form.newRecord(empId, ditId)
		form.show()
		
	
	
	def newRecord(self):
		query = QtSql.QSqlQuery()
		query.prepare("""select min(beb_id) from beschaeftigungsbereiche""")
		query.exec_()
		query.next()
		minBebId = query.value(0).toInt()[0]
		
		query = QtSql.QSqlQuery()
		query.prepare("""select min(geh_id) from gehaelter""")
		query.exec_()
		query.next()
		minGehId = query.value(0).toInt()[0]
		
		rec = self.model.record()
		rec.setValue(self.model.fieldIndex('din_name'), '')
		rec.setValue(self.model.fieldIndex('din_gehalt'), 0.0)
		rec.setValue(self.model.fieldIndex('beb_bezeichnung'), QtCore.QVariant(minBebId))
		rec.setValue(self.model.fieldIndex('din_stundensatz'), 0.0)
		rec.setValue(self.model.fieldIndex('din_nummer'), -1)
		rec.setValue(self.model.fieldIndex('geh_kbez'), minGehId)
		#self.model.insertRecord(-1, rec)
		self.model.insertRowIntoTable(rec)
		self.model.select()
		
		
	def deleteRecord(self):
		selected = self.tableView.selectionModel().selectedRows(0);
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
		
	
