# -*- coding: utf-8 -*-
import datetime

from PyQt4 import QtCore, QtGui, QtSql

from forms.formBase import FormBase
from forms.dokumentDetail import DokumentDetailForm
from ui.forms.dokumenteForm_gui import Ui_DokumenteForm

import config

#class DateEditDelegate(QtGui.QItemDelegate):
#	
#	def createEditor(self, parent, option, index):
#		editor = QtGui.QDateEdit()
#		editor.setCalendarPopup(True)
#		editor.setDate(datetime.datetime.now())
#		return editor
		
#class LagerartikelDelegate(QtGui.QItemDelegate):
	
	#def createEditor(self, parent, option, index):
		#editor = QtGui.QComboBox()
		#return editor


class DokumenteForm(FormBase):
	
	uiClass = Ui_DokumenteForm
	ident = 'dokumente'
	
	def setupUi(self):
		super(DokumenteForm, self).setupUi()
		
		self.masterModel = QtSql.QSqlRelationalTableModel()
		self.masterModel.setTable('dokumente')
		self.masterModel.setRelation(self.masterModel.fieldIndex('dok_dotid'), QtSql.QSqlRelation('dokumenttypen', 'dot_id', 'dot_bezeichnung'))
		self.masterModel.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
		self.masterModel.setSort(2, QtCore.Qt.AscendingOrder)
		self.masterModel.select()
		
		
		#Master table
		#------------------------------
		# column headers
		self.masterModel.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
		self.masterModel.setHeaderData(1, QtCore.Qt.Horizontal, 'Typ')
		self.masterModel.setHeaderData(2, QtCore.Qt.Horizontal, 'Text')
		# table view
		self.masterTableView = self.ui.tableView_documents
		self.masterTableView.setModel(self.masterModel)
#		self.masterTableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.masterTableView))
#		self.masterTableView.setItemDelegateForColumn(2, DateEditDelegate())
		self.masterTableView.setColumnHidden(3, True)
		self.masterTableView.setColumnHidden(4, True)
		self.masterTableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.masterTableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.masterTableView.resizeColumnsToContents()
		self.masterTableView.horizontalHeader().setStretchLastSection(True)
		self.masterTableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		

	def setupSignals(self):
		super(DokumenteForm, self).setupSignals()
		self.connect(self.ui.pushButton_edit, QtCore.SIGNAL('clicked()'), self.editRecord)
		self.connect(self.ui.pushButton_new, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_delete, QtCore.SIGNAL('clicked()'), self.deleteRecord)
		self.connect(self.masterTableView.selectionModel(), QtCore.SIGNAL('selectionChanged(const QItemSelection&,const QItemSelection&)'), self._onMasterTableViewSelectionChanged)
		self.connect(self.masterTableView.tv, QtCore.SIGNAL('doubleClicked (const QModelIndex&)'), self._onMasterTableViewDoubleClicked)
		
	def _onMasterTableViewSelectionChanged(self, newSelection, oldSelection):
		self.displayDocImage()
		
	def _onMasterTableViewDoubleClicked(self, idx):
		self.editRecord()
		
	def editRecord(self, idx=None):
		if idx is None: idx = self.ui.tableView_documents.selectionModel().currentIndex()#.row()
		form = DokumentDetailForm(self)
		form.setModel(self.masterModel, idx)
		form.show()
		
	def newRecord(self):
		query = "select min(dot_id) from dokumenttypen"
		results = self.db.exec_(query)
		results.next()
		dotId = results.value(0).toInt()[0]
		
		m = self.masterModel
		record = m.record()
		record.setValue(m.fieldIndex('dot_bezeichnung'), QtCore.QVariant(dotId))
		record.setValue(m.fieldIndex('dok_datum'), QtCore.QVariant(datetime.datetime.now().strftime('%Y-%m-%d')))
		self.masterModel.insertRecord(-1, record)
		self.masterModel.submitAll()
		id_ = self.masterModel.query().lastInsertId().toInt()[0]
		idx = self.masterModel.match(self.masterModel.index(0,0), 0, id_)[0]
		idx = QtCore.QPersistentModelIndex(idx)
		self.editRecord(idx)#.row())
		
	
	def deleteRecord(self):
		reply = QtGui.QMessageBox.question(self, u'Löschen bestätigen',
				u"Datensatz wirklich löschen?", QtGui.QMessageBox.Yes | 
				QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.No:
			return
		id_ = self.getCurrentId()
		if id_:
			self.beginTransaction()
			query = "delete from dokumente where dok_id = %s" % (id_, )
			results = self.db.exec_(query)
			if results.lastError().isValid():
				print 'Error retrieving document:', results.lastError().text()
				self.rollback()
			else:
				idx = self.ui.tableView_documents.selectionModel().currentIndex()
				self.masterModel.removeRows(idx.row(), 1)
				self.masterModel.submitAll()
				self.commit()
	
	def displayDocImage(self):
		ba = self.getCurrentDocImage()
		if ba:
			pic = QtGui.QPixmap()
			pic.loadFromData(ba)
			self.ui.label_documentImage.setPixmap(self.scalePixmap(pic))
		
		
	def getCurrentDocImage(self):
		try:
			idx = self.ui.tableView_documents.selectionModel().currentIndex()
			ba = idx.sibling(idx.row(),4).data(QtCore.Qt.DisplayRole).toByteArray()
			if ba:
				return ba
			else:
				return False
		except:
			return False
			
	def scalePixmap(self, pm):
		return pm.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
		
		
	def getCurrentId(self):
		try:
			idx = self.ui.tableView_documents.selectionModel().currentIndex()
			id_, success = idx.sibling(idx.row(),0).data(QtCore.Qt.DisplayRole).toInt()
			if success:
				return id_
			else:
				return False
		except:
			return False
