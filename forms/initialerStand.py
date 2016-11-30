# -*- coding: utf-8 -*-
import decimal
import sys
import csv

from PyQt4 import QtCore, QtGui, QtSql

from lib.UnicodeWriter import UnicodeWriter
from forms.formBase import FormBase
from ui.forms.initialerStandForm_gui import Ui_InitialerStandForm
import config


class InitialerStandForm(FormBase):
	
	uiClass = Ui_InitialerStandForm
	ident = 'initialer_stand'
	
	
	def setupUi(self):
		super(InitialerStandForm, self).setupUi()
	
		self.model = QtSql.QSqlRelationalTableModel()
		self.model.setTable('initialer_stand')
		self.model.setRelation(self.model.fieldIndex('ist_artikel_id'), QtSql.QSqlRelation('artikel_basis', 'artikel_id', 'artikel_bezeichnung'))
		self.model.setRelation(self.model.fieldIndex('ist_periode_id'), QtSql.QSqlRelation('perioden', 'periode_id', 'periode_bezeichnung'))
		self.model.setRelation(self.model.fieldIndex('ist_arp_id'), QtSql.QSqlRelation('arbeitsplaetze', 'arp_id', 'arp_bezeichnung'))
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()
	
		# column headers
		self.model.setHeaderData(self.model.fieldIndex('ist_id'), QtCore.Qt.Horizontal, 'ID')
		self.model.setHeaderData(self.model.fieldIndex('artikel_bezeichnung'), QtCore.Qt.Horizontal, 'Artikel')
		self.model.setHeaderData(self.model.fieldIndex('ist_anzahl'), QtCore.Qt.Horizontal, 'Anzahl')
		self.model.setHeaderData(self.model.fieldIndex('arp_bezeichnung'), QtCore.Qt.Horizontal, 'Arbeitsplatz')
		self.model.setHeaderData(self.model.fieldIndex('periode_bezeichnung'), QtCore.Qt.Horizontal, 'Periode')
		

		
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
		model.setTable('arbeitsplaetze')
		model.select()
		
		self.ui.comboBox_workplace.setModel(model)
		self.ui.comboBox_workplace.setModelColumn(model.fieldIndex('arp_bezeichnung'))
		self.ui.comboBox_workplace.insertSeparator(-1)
		self.ui.comboBox_workplace.setCurrentIndex(-1)
		
		model = QtSql.QSqlTableModel()
		model.setTable('artikel_basis')
		model.select()
		self.filterArticleModel = model
		
		self.ui.comboBox_article.setModel(model)
		self.ui.comboBox_article.setModelColumn(model.fieldIndex('artikel_bezeichnung'))
		self.ui.comboBox_article.insertSeparator(-1)
		self.ui.comboBox_article.setCurrentIndex(-1)
		self.setArticleComboFilter()
		
		self.setFilter()
		
		
		
		
	def setupSignals(self):
		self.connect(self.ui.comboBox_period, QtCore.SIGNAL('currentIndexChanged(int)'), lambda: self.setArticleComboFilter() or self.setFilter())

		super(InitialerStandForm, self).setupSignals()

		self.connect(self.ui.pushButton_export, QtCore.SIGNAL('clicked()'),
                    self.exportData)
		self.connect(self.ui.pushButton_initPeriod, QtCore.SIGNAL('clicked()'), self._onInitPeriodBtnClicked)
		self.connect(self.ui.comboBox_workplace, QtCore.SIGNAL('currentIndexChanged(int)'), self.setFilter)
		self.connect(self.ui.comboBox_article, QtCore.SIGNAL('currentIndexChanged(int)'), self.setFilter)
		self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
		self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)

		
		
	def _onInitPeriodBtnClicked(self):
		query = QtSql.QSqlQuery()
		query.prepare("""insert into initialer_stand (ist_artikel_id, ist_anzahl, ist_arp_id, ist_periode_id)
					select lager_artikel_artikel, 0, arp_id, lager_artikel_periode from lager_artikel, arbeitsplaetze where lager_artikel_periode = ? and arp_bezeichnung like '%bar%'""")
		query.addBindValue(self.getCurrentPeriodId())
		query.exec_()
		query.next()

		if query.lastError().isValid():
			self.rollback()
			print 'Error while setting initial Stand:', query.lastError().text()
			QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
									'Initialer Stand konnte nicht gesetzt werden!\nBitte kontaktieren Sie Ihren Administrator.')
		else:
			self.commit()
	
		query = QtSql.QSqlQuery()
		query.prepare("""select periode_id from perioden, initialer_stand where ist_periode_id = periode_id and periode_id < ? order by periode_start desc limit 1""")
		query.addBindValue(self.getCurrentPeriodId())
		query.exec_()
		if query.size() > 0:
			query.next()
			prevPerId = query.value(0).toInt()[0]

			query = QtSql.QSqlQuery()
			query.prepare("""update initialer_stand as is1
							inner join (select ist_artikel_id as artid, ist_anzahl as anz, ist_arp_id as arpid
										from initialer_stand
										where 1=1
										and ist_periode_id = ?) as is2
										on is1.ist_artikel_id = is2.artid
							set is1.ist_anzahl = is2.anz
							where 1=1
							and is1.ist_arp_id = is2.arpid
							and is1.ist_periode_id = ?""")
			query.addBindValue(prevPerId)
			query.addBindValue(self.getCurrentPeriodId())
			query.exec_()
			query.next()

			if query.lastError().isValid():
				self.rollback()
				print 'Error while updating initial Stand:', query.lastError().text()
				QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
										'Initialer Stand konnte nicht aktualisiert werden!\nBitte kontaktieren Sie Ihren Administrator.')
			else:
				self.commit()
			
		self.model.select()
			
			
	def setFilter(self):
		articleClause = '' if self.ui.comboBox_article.currentIndex() <= 0 else 'and artikel_id = %s' % self.getPKForCombobox(self.ui.comboBox_article, 'artikel_id')
		workplaceClause = '' if self.ui.comboBox_workplace.currentIndex() <= 0 else 'and arp_id = %s' % self.getPKForCombobox(self.ui.comboBox_workplace, 'arp_id')
		self.model.setFilter('ist_periode_id=%(perId)s and artikel_periode=%(perId)s %(articleClause)s %(workplaceClause)s'%{'perId':self.getCurrentPeriodId(), 'articleClause': articleClause, 'workplaceClause': workplaceClause})
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
		
		query = QtSql.QSqlQuery()
		query.prepare("""select min(arp_id) from arbeitsplaetze where arp_bezeichnung like '%bar%'""")
		query.exec_()
		query.next()
		minArpId = query.value(0).toInt()[0]
		
		rec = self.model.record()
		rec.setValue(self.model.fieldIndex('artikel_bezeichnung'), minArticleId)
		rec.setValue(self.model.fieldIndex('ist_anzahl'), 0.0)
		rec.setValue(self.model.fieldIndex('arp_bezeichnung'), minArpId)
		rec.setValue(self.model.fieldIndex('periode_bezeichnung'), self.getCurrentPeriodId())
		#self.model.insertRecord(-1, rec)
		self.model.insertRowIntoTable(rec)
		self.model.select()
		self.tableView.scrollToBottom()
		
		
	def deleteRecord(self):
		selected = self.tableView.selectionModel().selectedRows(0);
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1);
		self.model.submitAll()
		
	

			

	def exportData(self):
		data = [["id", "amount"]]
		
		workplaceClause = '' if self.ui.comboBox_workplace.currentIndex() <= 0 else 'and ist_arp_id = %s' % self.getPKForCombobox(self.ui.comboBox_workplace, 'arp_id')
		
		query = QtSql.QSqlQuery()
		query.prepare("""select ist_artikel_id, ist_anzahl from initialer_stand where 1=1 and ist_periode_id = %s %s""" % (self.getCurrentPeriodId(), workplaceClause))
		query.exec_()
		while query.next():
			id_, amount = query.value(0).toInt()[0], query.value(1).toInt()[0]
			data.append([id_, amount])
		
		filename = QtGui.QFileDialog.getSaveFileName(self, 'Datei speichern',
				                                    '', 'CSV Files (*.csv)')
		with open(filename, 'wb') as f:
			writer = UnicodeWriter(f, delimiter="\t")
			writer.writerows(data)
