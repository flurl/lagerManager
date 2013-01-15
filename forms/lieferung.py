# -*- coding: utf-8 -*-
import datetime

from PyQt4 import QtCore, QtGui, QtSql

from forms.formBase import FormBase
from ui.forms.lieferungForm_gui import Ui_LieferungForm
from forms.lieferungDetail import LieferungDetailForm
import config

class DateEditDelegate(QtGui.QItemDelegate):
	
	def createEditor(self, parent, option, index):
		editor = QtGui.QDateEdit()
		editor.setCalendarPopup(True)
		editor.setDate(datetime.datetime.now())
		return editor
		
#class LagerartikelDelegate(QtGui.QItemDelegate):
	
	#def createEditor(self, parent, option, index):
		#editor = QtGui.QComboBox()
		#return editor


class LieferungForm(FormBase):
	
	uiClass = Ui_LieferungForm
	ident = 'lieferung'
	
	def setupUi(self):
		super(LieferungForm, self).setupUi()
		
		self.masterModel = QtSql.QSqlRelationalTableModel()
		self.masterModel.setTable('lieferungen')
		self.masterModel.setRelation(1, QtSql.QSqlRelation('lieferanten', 'lieferant_id', 'lieferant_name'))
		self.masterModel.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
		self.masterModel.setSort(2, QtCore.Qt.AscendingOrder)
		self.masterModel.select()
		
		#relationModel = self.masterModel.relationModel(1)
		#self.ui.comboBox_lieferant.setModel(relationModel)
		#self.ui.comboBox_lieferant.setModelColumn(relationModel.fieldIndex('lieferant_name'))
		

		
		self.detailModel = QtSql.QSqlRelationalTableModel()
		self.detailModel.setTable('lieferungen_details')
		self.detailModel.setRelation(1, QtSql.QSqlRelation('lieferungen', 'lieferung_id', 'datum'))
		self.detailModel.setRelation(2, QtSql.QSqlRelation('artikel_basis', 'artikel_id', 'artikel_bezeichnung'))
		self.detailModel.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
		self.detailModel.sort(self.detailModel.fieldIndex('lieferung_detail_id'), QtCore.Qt.AscendingOrder)
		
		
		#Master table
		#------------------------------
		# column headers
		self.masterModel.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
		self.masterModel.setHeaderData(1, QtCore.Qt.Horizontal, 'Lieferant')
		self.masterModel.setHeaderData(2, QtCore.Qt.Horizontal, 'Datum')
		# table view
		self.masterTableView = self.ui.tableView_lieferungen
		self.masterTableView.setModel(self.masterModel)
		self.masterTableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.masterTableView))
		self.masterTableView.setItemDelegateForColumn(2, DateEditDelegate())
		self.masterTableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.masterTableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.masterTableView.resizeColumnsToContents()
		self.masterTableView.horizontalHeader().setStretchLastSection(True)
		self.masterTableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		
		#detail table
		#--------------------------------
		# column headers
		self.detailModel.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
		self.detailModel.setHeaderData(1, QtCore.Qt.Horizontal, 'Lieferung')
		self.detailModel.setHeaderData(2, QtCore.Qt.Horizontal, 'Artikel')
		self.detailModel.setHeaderData(3, QtCore.Qt.Horizontal, 'Anzahl')
		# table view
		# ------------------------------------------------
		self.detailTableView = self.ui.tableView_lieferungenDetails
		self.detailTableView.setModel(self.detailModel)
		self.detailTableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.detailTableView))
		self.detailTableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.detailTableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.detailTableView.setColumnHidden(0, True)
		self.detailTableView.setColumnHidden(1, True)
		self.detailTableView.resizeColumnsToContents()
		self.detailTableView.horizontalHeader().setStretchLastSection(True)
		self.detailTableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		
		self.updateDetailFilter()
		

	def setupSignals(self):
		super(LieferungForm, self).setupSignals()
		self.connect(self.ui.radioButton_lieferung, QtCore.SIGNAL('toggled (bool)'), self.updateMasterFilter)
		self.connect(self.ui.comboBox_period, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateMasterFilter)
		self.connect(self.ui.pushButton_edit, QtCore.SIGNAL('clicked()'), self.editRecord)
		self.connect(self.ui.pushButton_new, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_delete, QtCore.SIGNAL('clicked()'), self.deleteRecord)
		self.connect(self.masterTableView.selectionModel(), QtCore.SIGNAL('selectionChanged(const QItemSelection&,const QItemSelection&)'), self._onMasterTableViewSelectionChanged)
		self.connect(self.masterTableView.tv, QtCore.SIGNAL('doubleClicked (const QModelIndex&)'), self._onMasterTableViewDoubleClicked)
		
	def _onMasterTableViewSelectionChanged(self, newSelection, oldSelection):
		self.updateDetailFilter()
		
	def _onMasterTableViewDoubleClicked(self, idx):
		self.editRecord()
		
	def editRecord(self, idx=None):
		form = LieferungDetailForm(self)
		
		if idx is None: 
			idx = self.currentSourceIndex()
		else:
			#idx has been supplied, so we assume, it's a new record from newRecord()'
			form.newRecord = True
		
		form.setModel(self.masterModel, idx)
		form.show()
		
	def newRecord(self):
		query = "select min(lieferant_id) from lieferanten"
		results = self.db.exec_(query)
		results.next()
		lieferantId = results.value(0).toInt()[0]
		
		fltr = self.masterModel.filter()
		self.masterModel.setFilter('')
		
		record = self.masterModel.record()
		record.setValue(1, QtCore.QVariant(lieferantId))
		record.setValue(2, QtCore.QVariant(datetime.datetime.now().strftime('%Y-%m-%d')))
		record.setValue(self.masterModel.fieldIndex('lie_ist_verbrauch'), QtCore.QVariant(0 if self.ui.radioButton_lieferung.isChecked() else 1))
		self.masterModel.insertRecord(-1, record)
		self.masterModel.submitAll()
		id_ = self.masterModel.query().lastInsertId().toInt()[0]
		idx = self.masterModel.match(self.masterModel.index(0,0), 0, id_)[0]
		idx = QtCore.QPersistentModelIndex(idx)
		self.editRecord(idx)#.row())
		self.masterModel.setFilter(fltr)
		
	
	def deleteRecord(self):
		reply = QtGui.QMessageBox.question(self, u'Löschen bestätigen',
				u"Datensatz wirklich löschen?", QtGui.QMessageBox.Yes | 
				QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.No:
			return
		id_ = self.getCurrentLieferungId()
		query = "delete from lieferungen_details where lieferung_id = %s" % (id_, )
		results = self.db.exec_(query)
		
		idx = self.currentSourceIndex()
		self.masterModel.removeRows(idx.row(), 1)
		self.masterModel.submitAll()
		
		
	def updateMasterFilter(self):
		print 'updateMasterFilter'
		query = QtSql.QSqlQuery()
		query.prepare("""select periode_start, periode_ende from perioden where periode_id = ?""")
		query.addBindValue(self.getCurrentPeriodId())
		query.exec_()
		query.next()
		start, ende = query.value(0).toDateTime(), query.value(1).toDateTime()
		self.masterModel.setFilter("lieferungen.lie_ist_verbrauch = %s and lieferungen.datum between '%s' and '%s'"%(0 if self.ui.radioButton_lieferung.isChecked() else 1, start.toPyDateTime().strftime('%Y-%m-%d %H:%M:%S'), ende.toPyDateTime().strftime('%Y-%m-%d %H:%M:%S')))
		self.masterModel.select()
	
		
	def updateDetailFilter(self):
		self.detailModel.setFilter('lieferungen_details.lieferung_id=%s and artikel_periode = %s'%(self.getCurrentLieferungId(), self.getCurrentPeriodId()))
		relModel = self.detailModel.relationModel(2)
		relModel.setFilter('artikel_periode = %s and artikel_id in (select lager_artikel_artikel from lager_artikel)'%self.getCurrentPeriodId())
		relModel.sort(1, QtCore.Qt.AscendingOrder)
		self.detailModel.select()
		self.detailTableView.resizeColumnsToContents()
		
	def getCurrentLieferungId(self):
		try:
			idx = self.ui.tableView_lieferungen.selectionModel().currentIndex()
			id_, success = idx.sibling(idx.row(),0).data(QtCore.Qt.DisplayRole).toInt()
			if success:
				return id_
			else:
				return False
		except:
			return False
		
		
	def currentSourceIndex(self):
		"""maps the current selection to the index of the proxy's current source"""
		idx = self.ui.tableView_lieferungen.selectionModel().currentIndex()#.row()
		idx = self.ui.tableView_lieferungen.model().mapToSource(idx)
		return idx
