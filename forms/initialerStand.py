# -*- coding: utf-8 -*-
import decimal
import sys

from PyQt4 import QtCore, QtGui, QtSql

from forms.formBase import FormBase
from ui.forms.initialerStandForm_gui import Ui_InitialerStandForm
import config


class InitialerStandForm(FormBase):
	
	uiClass = Ui_InitialerStandForm
	ident = 'initialer_standstand'
	
	
	def setupUi(self):
		super(InitialerStandForm, self).setupUi()
	
		self.model = QtSql.QSqlRelationalTableModel()
		self.model.setTable('initialer_stand')
		self.model.setRelation(self.model.fieldIndex('ist_artikel_id'), QtSql.QSqlRelation('artikel_basis', 'artikel_id', 'artikel_bezeichnung, ist_artikel_id'))
		self.model.setRelation(self.model.fieldIndex('ist_periode_id'), QtSql.QSqlRelation('perioden', 'periode_id', 'periode_bezeichnung'))
		self.model.setRelation(self.model.fieldIndex('ist_arp_id'), QtSql.QSqlRelation('arbeitsplaetze', 'arp_id', 'arp_bezeichnung'))
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()

		self.setFilter()
	
		# column headers
		self.model.setHeaderData(self.model.fieldIndex('ist_id'), QtCore.Qt.Horizontal, 'ID')
		self.model.setHeaderData(self.model.fieldIndex('ist_artikel_id'), QtCore.Qt.Horizontal, 'Artikel')
		self.model.setHeaderData(self.model.fieldIndex('ist_anzahl'), QtCore.Qt.Horizontal, 'Anzahl')
		self.model.setHeaderData(self.model.fieldIndex('ist_arp_id'), QtCore.Qt.Horizontal, 'Arbeitsplatz')
		self.model.setHeaderData(self.model.fieldIndex('ist_periode_id'), QtCore.Qt.Horizontal, 'Periode')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView_lagerstand
		self.tableView.setModel(self.model)
		self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.horizontalHeader().setStretchLastSection(True)
		
		self.connect(self.ui.pushButton_OK, QtCore.SIGNAL('clicked()'), self._onOKBtnClicked)
		self.connect(self.ui.pushButton_initPeriod, QtCore.SIGNAL('clicked()'), self._onInitPeriodBtnClicked)
		self.connect(self.ui.comboBox_period, QtCore.SIGNAL('currentIndexChanged(int)'), self.setFilter)
		
		
	def setupSignals(self):
		super(InitialerStandForm, self).setupSignals()
		self.connect(self.ui.pushButton_export, QtCore.SIGNAL('clicked()'),
                    self.exportData)

		
	def _onOKBtnClicked(self):
		self.accept()
		
		
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
		self.model.setFilter('ist_periode_id=%(perId)s and artikel_periode=%(perId)s'%{'perId':self.getCurrentPeriodId()})
		self.model.select()
			

	def exportData(self):
		model = self.tableView.model()
		rows = model.rowCount()

		for i in range(rows):
			print model.data(model.index(i, self.model.fieldIndex("ist_artikel_id")), QtCore.Qt.DisplayRole).toString()
			print model.data(model.index(i, self.model.fieldIndex("ist_anzahl")), QtCore.Qt.DisplayRole).toString()

		return

		filename = QtGui.QFileDialog.getSaveFileName(self, 'Datei speichern',
				                                    '', 'CSV Files (*.csv)')
		with open(filename, 'wb') as f:
			writer = UnicodeWriter(f)
			writer.writerows(data)
