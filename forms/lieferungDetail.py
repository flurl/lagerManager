# -*- coding: utf-8 -*-
#import datetime
import codecs

from PyQt4 import QtCore, QtGui, QtSql

from forms.formBase import FormBase
from ui.forms.lieferungDetailForm_gui import Ui_LieferungDetailForm

import config
from CONSTANTS import *
import DBConnection

from lib.NullDelegate import NullDelegate
from lib.ImageViewer import ImageViewer
from lib.ClickableLabel import ClickableLabel


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
		self.docImages = []
		self.documentChanged = False
		self.newRecord = False
		self.grossTextEdited = False
		
	def setupUi(self):
		super(LieferungDetailForm, self).setupUi()
		
		self.ui.dateTimeEdit_flag.hide()
		
		self.detailModel = QtSql.QSqlRelationalTableModel()
		self.detailModel.setTable('lieferungen_details')
		self.detailModel.setRelation(1, QtSql.QSqlRelation('lieferungen', 'lieferung_id', 'datum'))
		self.detailModel.setRelation(2, QtSql.QSqlRelation('artikel_basis', 'artikel_id', 'artikel_bezeichnung'))
		self.detailModel.setRelation(self.detailModel.fieldIndex('lde_stsid'), QtSql.QSqlRelation('steuersaetze', 'sts_id', 'sts_bezeichnung'))
		self.detailModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.detailModel.sort(self.detailModel.fieldIndex('lieferung_detail_id'), QtCore.Qt.AscendingOrder)
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
		
		self.createContextMenu()
		

	def setupSignals(self):
		#super(LieferungDetailForm, self).setupSignals()
		self.connect(self.ui.pushButton_newDetail, QtCore.SIGNAL('clicked()'), self.addDetail)
		self.connect(self.ui.pushButton_deleteDetail, QtCore.SIGNAL('clicked()'), self.deleteDetail)
		self.connect(self.ui.pushButton_addDocument, QtCore.SIGNAL('clicked()'), self.chooseFile)
		self.connect(self.ui.pushButton_selectArticles, QtCore.SIGNAL('clicked()'), self.openArticleSelection)
		self.connect(self.ui.pushButton_updateFlag, QtCore.SIGNAL('clicked()'), lambda: (self.ui.dateTimeEdit_flag.setDateTime(QtCore.QDateTime.currentDateTime()), self.accept()))
		#self.connect(self.ui.lineEdit_dokId, QtCore.SIGNAL('textChanged (const QString&)'), self.displayImageFromDb)
		#self.connect(self.ui.label_document, QtCore.SIGNAL('clicked()'), self.showImage)
		self.connect(self.detailModel, QtCore.SIGNAL('dataChanged(const QModelIndex&,const QModelIndex&)'), self.articleChanged)
		self.connect(self.ui.tableView_details.selectionModel(), QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'), self.detailSelectionChanged)
		self.connect(self.ui.lineEdit_totalNet, QtCore.SIGNAL('textEdited(const QString&)'), self.onNetTextEdited)
		self.connect(self.ui.lineEdit_totalGross, QtCore.SIGNAL('textEdited(const QString&)'), self.onGrossTextEdited)
		
		
	def createContextMenu(self):
	
		#taxes context menu
		query = QtSql.QSqlQuery()
		query.prepare('select sts_bezeichnung, sts_prozent, sts_id from steuersaetze')
		query.exec_()
		if query.lastError().isValid():
			print 'Error selecting taxes for context menu:', query.lastError().text()
		else:
			actions = []
			while query.next():
				bez = query.value(0).toString()
				percent = query.value(1).toFloat()[0]
				stsId = query.value(2).toInt()[0]
				actions.append(QtGui.QAction(bez, self))
				self.connect(actions[-1], QtCore.SIGNAL('triggered()'), lambda sId=stsId: self.calcNetPrice(sId))
				self.detailTableView.addAction(actions[-1])
				
		sep = QtGui.QAction(self)
		sep.setSeparator(True)
		self.detailTableView.addAction(sep)
				
		#liefereinheiten context menu
		query = QtSql.QSqlQuery()
		query.prepare('select lei_bezeichnung, lei_menge from liefereinheiten')
		query.exec_()
		if query.lastError().isValid():
			print 'Error selecting delivery units for context menu:', query.lastError().text()
		else:
			actions = []
			while query.next():
				bez = query.value(0).toString()
				amount = query.value(1).toFloat()[0]
				actions.append(QtGui.QAction(bez, self))
				self.connect(actions[-1], QtCore.SIGNAL('triggered()'), lambda a=amount: self.calcAmountPrice(a))
				self.detailTableView.addAction(actions[-1])
				
		sep = QtGui.QAction(self)
		sep.setSeparator(True)
		self.detailTableView.addAction(sep)
		
		divideAction = QtGui.QAction(u'Durch Anzahl dividieren', self)
		self.connect(divideAction, QtCore.SIGNAL('triggered()'), self.divideByAmount)
		self.detailTableView.addAction(divideAction)
		
		sep = QtGui.QAction(self)
		sep.setSeparator(True)
		self.detailTableView.addAction(sep)
		
		fillRemainingAction = QtGui.QAction(u'Artikel mit Restbetrag anlegen', self)
		self.connect(fillRemainingAction, QtCore.SIGNAL('triggered()'), self.createRemainingAmountArticle)
		self.detailTableView.addAction(fillRemainingAction)
				
		self.detailTableView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		

	def setModel(self, model, idx):
		self.index = idx
		self.model = model
		
		self.mapper = mapper = QtGui.QDataWidgetMapper()
		mapper.setModel(self.model)
		mapper.setCurrentIndex(idx.row())
		
		relationModel = self.model.relationModel(1)
		relationModel.setFilter('lieferanten.lft_ist_verbraucher = %s'%(1 if self.isVerbrauch() else 0,))
		self.ui.comboBox_lieferant.setModel(relationModel)
		self.ui.comboBox_lieferant.setModelColumn(relationModel.fieldIndex('lieferant_name'))
		
		
		mapper.setItemDelegate(NullDelegate(self.model))
		mapper.addMapping(self.ui.lineEdit_id, 0)
		mapper.addMapping(self.ui.comboBox_lieferant, 1)
		mapper.addMapping(self.ui.dateEdit_datum, 2)
		mapper.addMapping(self.ui.plainTextEdit_comment, self.model.fieldIndex('lie_kommentar'))
		mapper.addMapping(self.ui.lineEdit_totalNet, self.model.fieldIndex('lie_summe'))
		mapper.addMapping(self.ui.dateTimeEdit_flag, self.model.fieldIndex('lie_flag'))
		mapper.setSubmitPolicy(QtGui.QDataWidgetMapper.ManualSubmit)
		
		
		
		
		
		self.updateDetailFilter()
		self.detailTableView.resizeColumnsToContents()
		self.setupDocuments()
		
		if self.newRecord:
			self.ui.comboBox_lieferant.insertSeparator(-1)
			self.ui.comboBox_lieferant.setCurrentIndex(-1)
		
		#update the UI if this is a Verbrauch and not a lieferung
		if self.isVerbrauch():
			self.ui.groupBox_lieferung.setTitle(self.tr('Verbrauch'))
			self.ui.label_lieferant.setText(self.tr('Verbraucher'))
			
		self.calcTotal()
		
			
	def accept(self):
		if self.isVerbrauch():
			alreadyAsked = False
			for row in range(0, self.detailModel.rowCount()):
				record = self.detailModel.record(row)
				value = record.value(self.detailModel.fieldIndex('anzahl')).toFloat()[0]
				if value >= 0.0:
					if not alreadyAsked:
						answer = QtGui.QMessageBox.question(self, u'Mengen Fehler', 
								u'Verbrauch Mengen müssen negativ sein! Alle positiven eingegeben Mengen werden automatisch mit -1 multipliziert.\nFortfahren?',
								QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
						alreadyAsked = True
						if answer == QtGui.QMessageBox.No:
							return False
					
					record.setValue('anzahl', QtCore.QVariant(value*-1))
					self.detailModel.setRecord(row, record)

	
		if self.ui.comboBox_lieferant.currentText().isEmpty():
			QtGui.QMessageBox.warning(self, u'Lieferanten Fehler', u'Kein Lieferant ausgewählt!')
			return False
		
		pStart, pEnd = self.getCurrentPeriodStartEnd()
		date = self.ui.dateEdit_datum.date().toPyDate()
		if pStart > date or date > pEnd:
			QtGui.QMessageBox.warning(self, u'Perioden Fehler', u'Das Lieferungsdatum liegt nicht innerhalb der gewählten Periode!')
			return False
			
			
		if self.lieferungForDayExists():
			answer = QtGui.QMessageBox.question(self, u'Lieferanten Fehler', 
							u'Es existiert bereits eine Lieferung/ein Verbrauch dieses Lieferanten/Verbrauchers für diesen Tag!\nTrotzdem fortfahren?',
							QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
			if answer == QtGui.QMessageBox.No:
				return False
				
		self.saveDocuments()
		self.mapper.submit()
		self.model.submitAll()
		super(LieferungDetailForm, self).accept()
		
	def reject(self):
		self.model.revertAll()
		if self.newRecord:
			id_ = self.getCurrentLieferungId()

			self.beginTransaction()
			query = QtSql.QSqlQuery()
			query.prepare('delete from lieferungen_details where lieferung_id = ?')
			query.addBindValue(id_)
			query.exec_()
			if query.lastError().isValid():
				self.rollback()
				print 'Error deleting lieferung details for lieferung with id %s:'%(id_, ), query.lastError().text()
				QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
										'Datensatz konnte nicht gelöscht werden!\nBitte kontaktieren Sie Ihren Administrator.')
			else:
				query = QtSql.QSqlQuery()
				query.prepare('delete from lieferungen where lieferung_id = ?')
				query.addBindValue(id_)
				query.exec_()
				if query.lastError().isValid():
					self.rollback()
					print 'Error deleting lieferung with id %s:'%(id_, ), query.lastError().text()
					QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
											'Datensatz konnte nicht gelöscht werden!\nBitte kontaktieren Sie Ihren Administrator.')
				else:
					self.commit()

		self.model.select()

		super(LieferungDetailForm, self).reject()
		
		
	def addDetail(self, artikelId=None, anzahl=None, einkaufspreis=None, stsId=None):
		lieferungId = self.getCurrentLieferungId()
		
		if artikelId is None:
			query = "select min(lager_artikel_artikel) from lager_artikel where lager_artikel_periode = %s" % (self.getCurrentPeriodId(), )
			results = self.db.exec_(query)
			results.next()
			artikelId = results.value(0).toInt()[0]
		
		if not artikelId:
			QtGui.QMessageBox.warning(self, u'Lagerartikel Fehler', u'Kein Lagerartikel für die gewählte Periode gefunden!')
			return False
		
		if stsId is None:
			query = "select sts_id from steuersaetze where sts_bezeichnung = 'null'"
			results = self.db.exec_(query)
			results.next()
			stsId = results.value(0).toInt()[0]
		
		if not stsId:
			QtGui.QMessageBox.warning(self, u'Steuersatz Fehler', u'Null Steuersatz nicht gefunden!')
			return False
		
		if anzahl is None:
			anzahl = 1.0
		
		if einkaufspreis is None:
			einkaufspreis = 0.0
		
		query = """insert into lieferungen_details (lieferung_id, artikel_id, anzahl, einkaufspreis, lde_stsid) 
				values 
				(%s, %s, %s, %s, %s)""" % (lieferungId, artikelId, anzahl, einkaufspreis, stsId)
		results = self.db.exec_(query)
		self.db.commit()
		self.detailModel.select()
		self.detailTableView.resizeColumnsToContents()
		self.ui.tableView_details.scrollToBottom()
		
		
	def deleteDetail(self):
		selected = self.detailTableView.selectionModel().selectedRows()
		for i in range(len(selected)):
			self.detailModel.removeRows(selected[i].row(), 1)
		self.detailModel.submitAll()
		
	def getCurrentLieferungId(self):
		id_ = self.model.record(self.mapper.currentIndex()).value(0).toInt()[0]
		return id_
		
	def getCurrentLieferantId(self):
		cb = self.ui.comboBox_lieferant
		cbModel = cb.model()
		lieferantId, ok = cbModel.record(cb.currentIndex()).value(0).toInt()
		if not ok:
			return -1
		return lieferantId
		
	def isVerbrauch(self):
		istVerbrauch = self.model.record(self.mapper.currentIndex()).value(self.model.fieldIndex('lie_ist_verbrauch')).toInt()[0]
		return True if istVerbrauch else False
		
	def updateDetailFilter(self):
		try:
			excludeArticles = config.config['connection'][DBConnection.connName]['period'][unicode(self.getCurrentPeriodId())]['exclude_articles']
		except KeyError:
			excludeArticles = []
		#in the config they are saved as strings
		excludeArticles = [int(a) for a in excludeArticles]	
		
		excludeArticles.insert(0,-1)
		excludeArticles.append(-1)
		excludeArticles = tuple(excludeArticles)
		
		relModel = self.detailModel.relationModel(2)
		relModel.setFilter('artikel_id in (select lager_artikel_artikel from lager_artikel where lager_artikel_periode = %(perId)s and lager_artikel_artikel not in %(excludeArticles)s) and artikel_periode = %(perId)s'% {'perId':self.getCurrentPeriodId(), 'excludeArticles': excludeArticles})
		relModel.sort(1, QtCore.Qt.AscendingOrder)
	
		self.detailModel.setFilter('lieferungen_details.lieferung_id=%s and artikel_periode = %s'%(self.getCurrentLieferungId(), self.getCurrentPeriodId()))
		self.detailModel.select()
		
	def getCurrentPeriodId(self):
		return self.currentPeriod
		
		
	def chooseFile(self):
		fileName = QtGui.QFileDialog.getOpenFileName(self, self.tr("Open Image"), "", self.tr("Image Files (*.png *.jpg *.bmp)"))
		"""image = QtGui.QImage(fileName)
		pic = QtGui.QPixmap.fromImage(image)
		self.ui.label_document.setPixmap(self.scalePixmap(pic)) #Put image into QLabel object
		"""
		
		#load image to bytearray
		ba = QtCore.QByteArray()
		f = QtCore.QFile(fileName)
		if f.open(QtCore.QIODevice.ReadOnly):
			ba = f.readAll()
			f.close()
			#self.docImage = ba
			
			#if an .txt with the same name exists, use that as source for the text data
			try:
				ocr = ''
				fileName, ext = os.path.splitext(str(fileName))
				with codecs.open(fileName+'.txt', 'r', 'utf-8') as f:
					ocr = f.read()
			except IOError as e:
				print 'No text file found'
			
			doc = {'id': None, 'status': 'new', 'byteArray': ba, 'ocr': ocr}
			self.docImages.append(doc)
			self.addDocumentLayout(doc)
			self.documentChanged = True
			
			
	def setupDocuments(self):
		query = QtSql.QSqlQuery()
		query.prepare('select dok_id from dokumente where dok_lieferung_id = ?')
		query.addBindValue(self.getCurrentLieferungId())
		query.exec_()
		if query.lastError().isValid():
			print 'Error while selecting documents'
		else:
			while query.next():
				dokId, ok = query.value(0).toInt()
				if ok and dokId > 0:
					self.displayImageFromDb(dokId)

	def saveDocuments(self):
		if self.documentChanged:
			for imgStruct in self.docImages:
				if imgStruct['status'] == 'new':
					#Writing the image into table
					self.beginTransaction()
					query = QtSql.QSqlQuery()
					query.prepare('insert into dokumente (dok_dotid, dok_bezeichnung, dok_data, dok_ocr, dok_lieferung_id) values (?, ?, ?, ?, ?)')
					query.addBindValue(EINGANGSRECHNUNGID)
					query.addBindValue('Lieferung-%s'%(self.getCurrentLieferungId(), ))
					query.addBindValue(imgStruct['byteArray'])
					query.addBindValue(imgStruct['ocr'])
					query.addBindValue(self.getCurrentLieferungId())
					query.exec_()
					if query.lastError().isValid():
						print 'Error inserting image:', query.lastError().text()
						self.rollback()
					else:
						self.commit()
						#self.ui.lineEdit_dokId.setText(query.lastInsertId().toString())
			
				#update the document in db if only the text changed
				elif imgStruct['status'] == 'removed':
					self.beginTransaction()
					query = QtSql.QSqlQuery()
					query.prepare('update dokumente set dok_lieferung_id = null where dok_id = ?')
					query.addBindValue(imgStruct['id'])
					query.exec_()
					if query.lastError().isValid():
						print 'Error removing document:', query.lastError().text()
						self.rollback()
					else:
						self.commit()
				
				
	def removeDocument(self, doc, layout):
		doc['status'] = 'removed'
		for i in range(layout.count()): layout.itemAt(i).widget().close()
		self.documentChanged = True
				
	
	def displayImageFromDb(self, dokId):
		query = QtSql.QSqlQuery()
		query.prepare('select dok_data, dok_ocr from dokumente where dok_id = ?')
		query.addBindValue(dokId)
		query.exec_()
		query.next()
		if query.lastError().isValid():
			print 'Error retrieving document:', query.lastError().text()
		else:
			doc = {'id': dokId, 'status': 'unmodified', 'ocr': query.value(1).toString(), 'byteArray': query.value(0).toByteArray()}
			self.docImages.append(doc)
			self.addDocumentLayout(doc)
			
			
	def addDocumentLayout(self, doc):
		docLayout = self.ui.layout_documents
		
		layout = QtGui.QVBoxLayout()
		
		label = ClickableLabel()
		
		#ba = query.value(0).toByteArray()
		ba = doc['byteArray']
		pic = QtGui.QPixmap()
		pic.loadFromData(ba)
		
		#Show the image into a QLabel object
		label.setPixmap(self.scalePixmap(pic))
		self.connect(label, QtCore.SIGNAL('clicked()'), lambda ba=ba: self.showImage(ba))
		
		delBtn = QtGui.QPushButton(u'löschen')
		self.connect(delBtn, QtCore.SIGNAL('clicked()'), lambda doc=doc, l=layout: self.removeDocument(doc, layout))
		
		layout.addWidget(label)
		layout.addWidget(delBtn)
		
		docLayout.addLayout(layout)
		
		#set the text
		#text = query.value(1).toString()
		#self.ui.plainTextEdit_ocr.setPlainText(text)
			
	def scalePixmap(self, pm):
		return pm.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)

	def showImage(self, byteArray):
		if byteArray is not None:
			pic = QtGui.QPixmap()
			pic.loadFromData(byteArray)
			viewer = ImageViewer(self)
			viewer.setPixmap(pic)
			viewer.show()
	
	def lieferungForDayExists(self):
		query = QtSql.QSqlQuery()
		query.prepare('select count(*) from lieferungen where lieferant_id = ? and date(datum) = date(?) and lieferung_id != ?')
		query.addBindValue(self.getCurrentLieferantId())
		query.addBindValue(self.ui.dateEdit_datum.dateTime())
		query.addBindValue(self.getCurrentLieferungId())
		query.exec_()
		if query.lastError().isValid():
			print 'Error while getting count of lieferungen for that day:', query.lastError().text()
		query.next()
		count = query.value(0).toInt()[0]
		if count != 0:
			return True
		else:
			return False
	
		
	def calcNetPrice(self, stsId):
		query = QtSql.QSqlQuery()
		query.prepare('select sts_bezeichnung, sts_prozent, sts_id from steuersaetze where sts_id = ?')
		query.addBindValue(stsId)
		query.exec_()
		if query.lastError().isValid():
			print 'Error selecting tax for calculating net price:', query.lastError().text()
			return
		
		query.next()
		bez = query.value(0).toString()
		percent = query.value(1).toFloat()[0]
		stsId = query.value(2).toInt()[0]
				
		idxList = self.detailTableView.selectedIndexes()
		idx = idxList[0]
		idx = idx.sibling(idx.row(), 4)
		value = self.detailModel.data(idx)
		value = QtCore.QVariant(value.toFloat()[0]/(100+percent)*100)
		self.detailModel.setData(idx, value)
		
		#set tax foreign key
		idx = idx.sibling(idx.row(), self.detailModel.fieldIndex('sts_bezeichnung'))
		self.detailModel.setData(idx, stsId)
		
	def calcAmountPrice(self, amount):
		idxList = self.detailTableView.selectedIndexes()
		idx = idxList[0]
		idx = idx.sibling(idx.row(), 4)
		value = self.detailModel.data(idx)
		value = QtCore.QVariant(value.toFloat()[0]/amount)
		self.detailModel.setData(idx, value)
		
	def divideByAmount(self):
		idxList = self.detailTableView.selectedIndexes()
		idx = idxList[0]
		valueIdx = idx.sibling(idx.row(), 4)
		amountIdx = idx.sibling(idx.row(), 3)
		value = self.detailModel.data(valueIdx)
		amount = self.detailModel.data(amountIdx)
		value = QtCore.QVariant(value.toFloat()[0]/amount.toFloat()[0])
		self.detailModel.setData(valueIdx, value)
		
		
	def createRemainingAmountArticle(self):
		grossTotal = self.calcTotal()['gross']
		enteredTotal = self.ui.lineEdit_totalGross.text().toFloat()[0]
		diff = enteredTotal-grossTotal
		self.addDetail(einkaufspreis=diff)
		self.grossTextEdited = False
		
		
	def openArticleSelection(self):
		import forms.lagerartikelAuswahl
		form = forms.lagerartikelAuswahl.LagerartikelAuswahlForm(self)
		form.exec_()
		
		
	def articleChanged(self, topLeft, topRight):
		self.updateUnitDisplay(topLeft)
		self.calcTotal()
		
	def detailSelectionChanged(self, selected, deselected):
		indexes = selected.indexes()
		if len(indexes) > 0:
			index = indexes[0]
			self.updateUnitDisplay(index)
		
	def updateUnitDisplay(self, index):
		model = index.model()
		detailId = model.data(model.index(index.row(), 0)).toInt()[0]
		
		query = QtSql.QSqlQuery()
		query.prepare("""select lager_einheit_name 
						from lieferungen_details, lager_artikel, lager_einheiten 
						where 1=1
						and lieferungen_details.artikel_id = lager_artikel.lager_artikel_artikel
						and lager_artikel_einheit = lager_einheit_id
						and lieferung_detail_id = %(detailId)s
						and lager_artikel_periode = %(perId)s
						and lager_einheit_periode = %(perId)s""" % {'detailId': detailId, 'perId':self.getCurrentPeriodId()})
		#query.addBindValue(self.getCurrentLieferantId())
		#query.addBindValue(self.ui.dateEdit_datum.dateTime())
		#query.addBindValue(self.getCurrentLieferungId())
		query.exec_()
		if query.lastError().isValid():
			print 'Error while getting count of lieferungen for that day:', query.lastError().text()
		query.next()
		unit = query.value(0).toString()
		self.ui.label_unit.setText('Einheit: '+unit)
		
		
	def onGrossTextEdited(self, text):
		print 'onGrossTextChanged'
		self.grossTextEdited = True
		
	def onNetTextEdited(self, text):
		print 'onNetTextChanged'
		
	
	def calcTotal(self):
		query = QtSql.QSqlQuery()
		query.prepare("""select round(sum(anzahl*einkaufspreis), 2), round(sum(anzahl*(einkaufspreis*(100+sts_prozent)/100)), 2)
						from lieferungen_details, steuersaetze
						where 1=1
						and lde_stsid = sts_id
						and lieferungen_details.lieferung_id = ?""")
		query.addBindValue(self.getCurrentLieferungId())
		query.exec_()
		if query.lastError().isValid():
			print 'Error while getting sum of lieferungen details:', query.lastError().text()
			return
		query.next()
		netTotal = query.value(0).toString()
		grossTotal = query.value(1).toString()
		self.ui.lineEdit_totalNet.setText(netTotal)
		if not self.grossTextEdited:
			self.ui.lineEdit_totalGross.setText(grossTotal)
			
		return {'net':netTotal.toFloat()[0], 'gross': grossTotal.toFloat()[0]}
		
		
	
		
		