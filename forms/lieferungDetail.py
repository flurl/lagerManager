# -*- coding: utf-8 -*-
#import datetime

from PyQt4 import QtCore, QtGui, QtSql

from forms.formBase import FormBase
from ui.forms.lieferungDetailForm_gui import Ui_LieferungDetailForm

import config
from CONSTANTS import *


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
	
	def __init__(self, parent):
		FormBase.__init__(self, parent)
		self.docImage = None
		self.documentChanged = False
		
	def setupUi(self):
		super(LieferungDetailForm, self).setupUi()
		
		self.detailModel = QtSql.QSqlRelationalTableModel()
		self.detailModel.setTable('lieferungen_details')
		self.detailModel.setRelation(1, QtSql.QSqlRelation('lieferungen', 'lieferung_id', 'datum'))
		self.detailModel.setRelation(2, QtSql.QSqlRelation('artikel_basis', 'artikel_id', 'artikel_bezeichnung'))
		self.detailModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		#self.detailModel.select()
		
		self.detailTableView = self.ui.tableView_details
		self.detailTableView.setModel(self.detailModel)
		self.detailTableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.detailTableView))
		self.detailTableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.detailTableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.detailTableView.setColumnHidden(0, True)
		self.detailTableView.setColumnHidden(1, True)
		self.detailTableView.resizeColumnsToContents()
		self.detailTableView.horizontalHeader().setStretchLastSection(True)
		

	def setupSignals(self):
		#super(LieferungDetailForm, self).setupSignals()
		self.connect(self.ui.pushButton_newDetail, QtCore.SIGNAL('clicked()'), self.addDetail)
		self.connect(self.ui.pushButton_deleteDetail, QtCore.SIGNAL('clicked()'), self.deleteDetail)
		self.connect(self.ui.pushButton_fileChooser, QtCore.SIGNAL('clicked()'), self.chooseFile)
		self.connect(self.ui.lineEdit_dokId, QtCore.SIGNAL('textChanged (const QString&)'), self.displayImageFromDb)
		self.connect(self.ui.label_document, QtCore.SIGNAL('clicked()'), self.showImage)
		

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
		mapper.addMapping(self.ui.lineEdit_dokId, self.model.fieldIndex('lie_dokid'))
		mapper.setSubmitPolicy(QtGui.QDataWidgetMapper.ManualSubmit)
		mapper.setCurrentIndex(idx.row())
		self.mapper = mapper
		
		self.updateDetailFilter()
		self.detailTableView.resizeColumnsToContents()
		
			
	def accept(self):
		self.saveDocument()
		self.mapper.submit()
		self.model.submitAll()
		super(LieferungDetailForm, self).accept()
		
	def reject(self):
		self.model.revertAll()
		super(LieferungDetailForm, self).reject()
		
		
	def addDetail(self):
		lieferungId = self.getCurrentLieferungId()
		
		query = "select min(lager_artikel_artikel) from lager_artikel where lager_artikel_periode = %s" % (self.getCurrentPeriodId(), )
		results = self.db.exec_(query)
		results.next()
		artikelId = results.value(0).toInt()[0]
		
		query = """insert into lieferungen_details (lieferung_id, artikel_id, anzahl, einkaufspreis) 
				values 
				(%s, %s, %s, %s)""" % (lieferungId, artikelId, 1.0, 0.0)
		print query
		results = self.db.exec_(query)
		self.db.commit()
		self.detailModel.select()
		self.detailTableView.resizeColumnsToContents()
		
		
	def deleteDetail(self):
		selected = self.detailTableView.selectionModel().selectedRows()
		for i in range(len(selected)):
			self.detailModel.removeRows(selected[i].row(), 1)
		self.detailModel.submitAll()
		
	def getCurrentLieferungId(self):
		id_ = self.model.record(self.mapper.currentIndex()).value(0).toInt()[0]
		#print 'lieferungID: ', id_, self.mapper.currentIndex(), self.model.record(self.mapper.currentIndex()).value(0)
		return id_
		
	def updateDetailFilter(self):
		relModel = self.detailModel.relationModel(2)
		relModel.setFilter('artikel_id in (select lager_artikel_artikel from lager_artikel where lager_artikel_periode = %(perId)s) and artikel_periode = %(perId)s'% {'perId':self.getCurrentPeriodId()})
		relModel.sort(1, QtCore.Qt.AscendingOrder)
	
		self.detailModel.setFilter('lieferungen_details.lieferung_id=%s and artikel_periode = %s'%(self.getCurrentLieferungId(), self.getCurrentPeriodId()))
		self.detailModel.select()
		
	def getCurrentPeriodId(self):
		query = QtSql.QSqlQuery()
		query.prepare('select periode_id from perioden where ? between periode_start and periode_ende' )
		query.addBindValue(QtCore.QVariant(self.ui.dateEdit_datum.date()))
		query.exec_()
		query.next()
		periodeId = query.value(0).toInt()[0]
		return periodeId
		
		
	def chooseFile(self):
		fileName = QtGui.QFileDialog.getOpenFileName(self, self.tr("Open Image"), "", self.tr("Image Files (*.png *.jpg *.bmp)"))
		print fileName
		image = QtGui.QImage(fileName)
		pic = QtGui.QPixmap.fromImage(image)
		self.ui.label_document.setPixmap(self.scalePixmap(pic)) #Put image into QLabel object
		
		#load image to bytearray
		ba = QtCore.QByteArray()
		f = QtCore.QFile(fileName)
		if f.open(QtCore.QIODevice.ReadOnly):
			ba = f.readAll()
			f.close()
			self.docImage = ba
			self.documentChanged = True

	def saveDocument(self):
		if self.documentChanged and self.docImage is not None:
			#Writing the image into table
			self.beginTransaction()
			query = QtSql.QSqlQuery()
			query.prepare('insert into dokumente (dok_dotid, dok_bezeichnung, dok_data) values (?, ?, ?)')
			query.addBindValue(EINGANGSRECHNUNGID)
			query.addBindValue('Lieferung-%s'%(self.getCurrentLieferungId(), ))
			query.addBindValue(self.docImage)
			query.exec_()
			if query.lastError().isValid():
				print 'Error inserting image:', query.lastError().text()
				self.rollback()
			else:
				self.commit()
				self.ui.lineEdit_dokId.setText(query.lastInsertId().toString())
	
	def displayImageFromDb(self):
		dokId = self.ui.lineEdit_dokId.text()
		dokId, ok = dokId.toInt()
		if ok and dokId > 0:
			query = QtSql.QSqlQuery()
			query.prepare('select dok_data from dokumente where dok_id = ?')
			query.addBindValue(dokId)
			query.exec_()
			query.next()
			if query.lastError().isValid():
				print 'Error retrieving document:', query.lastError().text()
			else:
				ba = query.value(0).toByteArray()
				self.docImage = ba
				pic = QtGui.QPixmap()
				pic.loadFromData(ba)
				#Show the image into a QLabel object
				self.ui.label_document.setPixmap(self.scalePixmap(pic))
			
	def scalePixmap(self, pm):
		return pm.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)

	def showImage(self):
		print 'clicked'
		if self.docImage is not None:
			print 'in if'
			label = QtGui.QLabel()
			pic = QtGui.QPixmap()
			pic.loadFromData(self.docImage)
			#Show the image into a QLabel object
			label.setPixmap(pic)
			
			area = QtGui.QScrollArea(self)
			area.setWidget(label)
			area.setWindowFlags(QtCore.Qt.Window)
			#label.setScaledContents(True)
			#label.resize(QtCore.QSize(350, 600))
			#label.show()
			area.showMaximized()
		
		
