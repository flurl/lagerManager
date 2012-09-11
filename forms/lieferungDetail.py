# -*- coding: utf-8 -*-
#import datetime

from PyQt4 import QtCore, QtGui, QtSql

from forms.formBase import FormBase
from ui.forms.lieferungDetailForm_gui import Ui_LieferungDetailForm
import config

#class DateEditDelegate(QtGui.QItemDelegate):
	
	#def createEditor(self, parent, option, index):
		#editor = QtGui.QDateEdit()
		#editor.setCalendarPopup(True)
		#editor.setDate(datetime.datetime.now())
		#return editor
		
#class LagerartikelDelegate(QtGui.QItemDelegate):
	
	#def createEditor(self, parent, option, index):
		#editor = QtGui.QComboBox()
		#return editor


class LieferungDetailForm(FormBase):
	
	uiClass = Ui_LieferungDetailForm
	ident = 'lieferungDetail'
	
	def setupUi(self):
		super(LieferungDetailForm, self).setupUi()
		
		self.detailModel = QtSql.QSqlRelationalTableModel()
		self.detailModel.setTable('lieferungen_details')
		self.detailModel.setRelation(1, QtSql.QSqlRelation('lieferungen', 'lieferung_id', 'datum'))
		self.detailModel.setRelation(2, QtSql.QSqlRelation('artikel_basis', 'artikel_id', 'artikel_bezeichnung'))
		relModel = self.detailModel.relationModel(2)
		relModel.setFilter('artikel_id in (select lager_artikel_artikel from lager_artikel)')
		relModel.sort(1, QtCore.Qt.AscendingOrder)
		self.detailModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.detailModel.select()
		
		self.detailTableView = self.ui.tableView_details
		self.detailTableView.setModel(self.detailModel)
		self.detailTableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.detailTableView))
		self.detailTableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.detailTableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.detailTableView.resizeColumnsToContents()
		self.detailTableView.horizontalHeader().setStretchLastSection(True)
		

	def setupSignals(self):
		#super(LieferungDetailForm, self).setupSignals()
		self.connect(self.ui.pushButton_newDetail, QtCore.SIGNAL('clicked()'), self.addDetail)
		self.connect(self.ui.pushButton_deleteDetail, QtCore.SIGNAL('clicked()'), self.deleteDetail)
		

	def setModel(self, model, idx):
		print 'setModel:', model, idx, idx.row()
		self.index = idx
		self.model = model
		relationModel = self.model.relationModel(1)
		self.ui.comboBox_lieferant.setModel(relationModel)
		self.ui.comboBox_lieferant.setModelColumn(relationModel.fieldIndex('lieferant_name'))
		
		mapper = QtGui.QDataWidgetMapper()
		mapper.setModel(self.model)
		mapper.setItemDelegate(QtSql.QSqlRelationalDelegate(self.model))
		mapper.addMapping(self.ui.lineEdit_id, 0)
		mapper.addMapping(self.ui.comboBox_lieferant, 1)
		mapper.addMapping(self.ui.dateEdit_datum, 2)
		mapper.setSubmitPolicy(QtGui.QDataWidgetMapper.ManualSubmit)
		mapper.setCurrentIndex(idx.row())
		self.mapper = mapper
		
		self.updateDetailFilter()
		
			
	def accept(self):
		self.mapper.submit()
		self.model.submitAll()
		super(LieferungDetailForm, self).accept()
		
	def reject(self):
		self.model.revertAll()
		super(LieferungDetailForm, self).reject()
		
		
	def addDetail(self):
		lieferungId = self.getCurrentLieferungId()
		
		query = "select min(lager_artikel_artikel) from lager_artikel"
		results = self.db.exec_(query)
		results.next()
		artikelId = results.value(0).toInt()[0]
		
		query = """insert into lieferungen_details (lieferung_id, artikel_id, anzahl, einkaufspreis) 
				values 
				(%s, %s, %s, %s)""" % (lieferungId, artikelId, 1.0, 1.0)
		print query
		results = self.db.exec_(query)
		self.db.commit()
		self.detailModel.select()
		
		
	def deleteDetail(self):
		selected = self.detailTableView.selectionModel().selectedRows()
		for i in range(len(selected)):
			self.detailModel.removeRows(selected[i].row(), 1)
		self.detailModel.submitAll()
		
	def getCurrentLieferungId(self):
		id_ = self.model.record(self.mapper.currentIndex()).value(0).toInt()[0]
		print 'lieferungID: ', id_, self.mapper.currentIndex(), self.model.record(self.mapper.currentIndex()).value(0)
		return id_
		
	def updateDetailFilter(self):
		self.detailModel.setFilter('lieferungen_details.lieferung_id=%s'%(self.getCurrentLieferungId(),))
		self.detailModel.select()
		

