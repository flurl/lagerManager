# -*- coding: utf-8 -*-
import decimal
import sys
import csv
import datetime

from PyQt4 import QtCore, QtGui, QtSql

#from lib.UnicodeWriter import UnicodeWriter
from forms.formBase import FormBase
from ui.forms.gezaehlterStandForm_gui import Ui_GezaehlterStandForm
import config


class GezaehlterStandForm(FormBase):
	
	uiClass = Ui_GezaehlterStandForm
	ident = 'GezaehlterStand'
	
	
	def setupUi(self):
		super(GezaehlterStandForm, self).setupUi()
	
		self.model = QtSql.QSqlRelationalTableModel()
		self.model.setTable('gezaehlter_stand')
		self.model.setRelation(self.model.fieldIndex('gst_artikel_id'), QtSql.QSqlRelation('artikel_basis', 'artikel_id', 'artikel_bezeichnung'))
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()
	
		# column headers
		self.model.setHeaderData(self.model.fieldIndex('gst_id'), QtCore.Qt.Horizontal, 'ID')
		self.model.setHeaderData(self.model.fieldIndex('artikel_bezeichnung'), QtCore.Qt.Horizontal, 'Artikel')
		self.model.setHeaderData(self.model.fieldIndex('gst_anzahl'), QtCore.Qt.Horizontal, 'Anzahl')
		self.model.setHeaderData(self.model.fieldIndex('gst_datum'), QtCore.Qt.Horizontal, 'Datum')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView_lagerstand
		self.tableView.setModel(self.model)
		self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.horizontalHeader().setStretchLastSection(True)
		
		model = QtSql.QSqlTableModel()
		model.setTable('artikel_basis')
		model.select()
		self.filterArticleModel = model
		
		self.ui.comboBox_article.setModel(model)
		self.ui.comboBox_article.setModelColumn(model.fieldIndex('artikel_bezeichnung'))
		self.ui.comboBox_article.insertSeparator(-1)
		self.ui.comboBox_article.setCurrentIndex(-1)
		self.setArticleComboFilter()
		
		self.setupDateComboBox()
		
		self.ui.dateEdit_initDate.setDate(datetime.datetime.now())
		
		self.setFilter()
		
		
		
		
	def setupSignals(self):
		self.connect(self.ui.comboBox_period, QtCore.SIGNAL('currentIndexChanged(int)'), lambda: self.setArticleComboFilter() or self.setFilter())

		super(GezaehlterStandForm, self).setupSignals()

		"""self.connect(self.ui.pushButton_export, QtCore.SIGNAL('clicked()'),
                    self.exportData)"""
		self.connect(self.ui.pushButton_initPeriod, QtCore.SIGNAL('clicked()'), self._onInitDateBtnClicked)
		self.connect(self.ui.comboBox_date, QtCore.SIGNAL('currentIndexChanged(int)'), self.setFilter)
		self.connect(self.ui.comboBox_article, QtCore.SIGNAL('currentIndexChanged(int)'), self.setFilter)
		self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)


	def setupDateComboBox(self):
		print "setupDateComboBox"
		query = QtSql.QSqlQuery()
		query.prepare("select distinct gst_datum from gezaehlter_stand order by gst_datum desc")
		query.exec_()
		
		while query.next():
			date = query.value(0).toDateTime()
			dateStr = date.toPyDateTime().strftime("%Y-%m-%d")
			print date, dateStr
			self.ui.comboBox_date.addItem(dateStr, QtCore.QVariant(date))
		
		self.ui.comboBox_date.insertSeparator(-1)
		self.ui.comboBox_date.setCurrentIndex(-1)
		
		
	def _onInitDateBtnClicked(self):
		query = QtSql.QSqlQuery()
		query.prepare("""insert into gezaehlter_stand (gst_artikel_id, gst_anzahl, gst_datum)
					select lager_artikel_artikel, (select sum(ist_anzahl) from initialer_stand where ist_artikel_id = lager_artikel_artikel and ist_periode_id = lager_artikel_periode), ? from lager_artikel where lager_artikel_periode = ?""")
		query.addBindValue(self.ui.dateEdit_initDate.date())
		query.addBindValue(self.getCurrentPeriodId())
		query.exec_()
		query.next()

		if query.lastError().isValid():
			self.rollback()
			print 'Error while initializing date:', query.lastError().text()
			QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
									'Datum konnte nicht intialisiert werden!\nBitte kontaktieren Sie Ihren Administrator.')
		else:
			self.commit()
			
		self.model.select()
			
			
	def setFilter(self):
		articleClause = '' if self.ui.comboBox_article.currentIndex() <= 0 else 'and artikel_id = %s' % self.getPKForCombobox(self.ui.comboBox_article, 'artikel_id')
		dateClause = '' if self.ui.comboBox_date.currentIndex() <= 0 else 'and gst_datum = "%s"' % self.ui.comboBox_date.itemData(self.ui.comboBox_date.currentIndex()).toDateTime().toPyDateTime().strftime("%Y-%m-%d")
		self.model.setFilter('artikel_periode=%(perId)s %(articleClause)s %(dateClause)s'%{'perId':self.getCurrentPeriodId(), 'articleClause': articleClause, 'dateClause': dateClause})
		self.model.select()
		
	def setArticleComboFilter(self):
		self.filterArticleModel.setFilter('artikel_periode = %s and artikel_id in (select lager_artikel_artikel from lager_artikel where lager_artikel_periode = %s)'%(self.getCurrentPeriodId(), self.getCurrentPeriodId()))
		self.filterArticleModel.select()
		self.ui.comboBox_article.insertSeparator(-1)
		self.ui.comboBox_article.setCurrentIndex(-1)
		
		
	def newRecord(self):
		query = QtSql.QSqlQuery()
		query.prepare("""select min(artikel_id) from artikel_basis 
						where 1=1
						and artikel_periode = %s 
						and artikel_id in (select lager_artikel_artikel from lager_artikel where lager_artikel_periode = %s)"""%(self.getCurrentPeriodId(), self.getCurrentPeriodId()))
		query.exec_()
		query.next()
		minArticleId = query.value(0).toInt()[0]
		
		rec = self.model.record()
		rec.setValue(self.model.fieldIndex('artikel_bezeichnung'), minArticleId)
		rec.setValue(self.model.fieldIndex('gst_anzahl'), 0.0)
		rec.setValue(self.model.fieldIndex('gst_datum'), datetime.datetime.now())
		#self.model.insertRecord(-1, rec)
		self.model.insertRowIntoTable(rec)
		self.model.select()
		self.tableView.scrollToBottom()
		
		
	def deleteRecord(self):
		selected = self.tableView.selectionModel().selectedRows(0);
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
		
	

			

	#def exportData(self):
	#	data = [["id", "amount"]]
	#	
	#	#workplaceClause = '' if self.ui.comboBox_date.currentIndex() <= 0 else 'and gst_arp_id = %s' % self.getPKForCombobox(self.ui.comboBox_date, 'arp_id')
	#	
	#	query = QtSql.QSqlQuery()
	#	query.prepare("""select gst_artikel_id, gst_anzahl from gezaehlter_stand where 1=1 and gst_periode_id = %s %s""" % (self.getCurrentPeriodId(), workplaceClause))
	#	query.exec_()
	#	while query.next():
	#		id_, amount = query.value(0).toInt()[0], query.value(1).toInt()[0]
	#		data.append([id_, amount])
	#	
	#	filename = QtGui.QFileDialog.getSaveFileName(self, 'Datei speichern',
	#			                                    '', 'CSV Files (*.csv)')
	#	with open(filename, 'wb') as f:
	#		writer = UnicodeWriter(f, delimiter="\t")
	#		writer.writerows(data)
