# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.verkaufteArtikelReport_gui import Ui_VerkaufteArtikelReport
from tableReport import TableReport



class VerkaufteArtikelReport(TableReport):
	
	uiClass = Ui_VerkaufteArtikelReport
	ident = 'verkaufteArtikel'
	
	def __init__(self, parent=None):
		TableReport.__init__(self, parent)
				
		self.setHeader('Verkaufte Artikel')
		self.setFooter('here could be a nice footer')
		
		self.setTableHeaders(['Datum', 'Kellner', 'Menge', 'Artikel', 'Preis', 'Artikelgruppe', 'Tisch', 'Zeit'])
		
		self.updateData()
		self.process()
		
	def setupUi(self):
		super(VerkaufteArtikelReport, self).setupUi()
		self.connect(self.ui.comboBox_period, QtCore.SIGNAL('currentIndexChanged(int)'), self.setupCPCombobox)
		self.setupCPCombobox()
		
	def setupCPCombobox(self):
		self.ui.comboBox_checkpoint.clear()
		
		query = "select checkpoint_id, checkpoint_info from journal_checkpoints where checkpoint_periode = %s" % self._getCurrentPeriodId()
		results = self.db.exec_(query)
		
		while results.next():
			id_ = results.value(0).toInt()[0]
			cp = results.value(1).toString()
			self.ui.comboBox_checkpoint.addItem(cp, QtCore.QVariant(int(id_)))
			
	def setupSignals(self):
		super(VerkaufteArtikelReport, self).setupSignals()
		self.connect(self.ui.comboBox_checkpoint, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
		self.connect(self.ui.radioButton_aufwand, QtCore.SIGNAL('toggled(bool)'), lambda checked: checked and self.updateData())
		self.connect(self.ui.radioButton_umsatz, QtCore.SIGNAL('toggled(bool)'), lambda checked: checked and self.updateData())
		self.connect(self.ui.radioButton_all, QtCore.SIGNAL('toggled(bool)'), lambda checked: checked and self.updateData())
		self.connect(self.ui.checkBox_showTableCode, QtCore.SIGNAL('toggled(bool)'), self.updateData)
		self.connect(self.ui.checkBox_showDate, QtCore.SIGNAL('toggled(bool)'), self.updateData)
		
	def updateData(self):
		data = []

		query =  self.mkQuery()
		print query
		results = self.db.exec_(query)
		
		lastDate = None
		
		while results.next():
			date = unicode(results.value(0).toString())
			waiter = unicode(results.value(1).toString())
			amount = round(results.value(2).toFloat()[0], 2)
			article = unicode(results.value(3).toString())
			price = round(results.value(4).toFloat()[0], 2)
			group = unicode(results.value(5).toString())
			
			index = 6
			if self.ui.checkBox_showTableCode.isChecked():
				table = unicode(results.value(index).toString())
				index += 1
			else:
				table = u''
			
			if self.ui.checkBox_showDate.isChecked():
				time = unicode(results.value(index).toString())
				index += 1
			else:
				time = u''
			
			if lastDate != date and lastDate is not None:
				data.append([None])
				lastDate = date
			data.append([date, waiter, amount, article, price, group, table, time])
		
		self.setData(data)
		self.process()
		
	
		
	def mkQuery(self):
		"""return the query"""
		
		umsatzWhere = ""
		if self.ui.radioButton_umsatz.isChecked():
			umsatzWhere = " and detail_istUmsatz = 1 "
		elif self.ui.radioButton_aufwand.isChecked():
			umsatzWhere = " and detail_istUmsatz = 0 "
			
		cpId = self.ui.comboBox_checkpoint.itemData(self.ui.comboBox_checkpoint.currentIndex()).toInt()[0]
		
		query = """
				select checkpoint_info, 
				detail_kellner, sum(detail_absmenge), detail_artikel_text, detail_preis, detail_gruppe %(table_code)s %(date)s
from journal_details, journal_daten, journal_checkpoints, rechnungen_basis
where 1=1
and (daten_checkpoint_tag = checkpoint_id or daten_checkpoint_monat = checkpoint_id or daten_checkpoint_jahr = checkpoint_id)
and detail_journal = daten_rechnung_id
and daten_rechnung_id = rechnung_id
and detail_periode = %(period_id)s
and daten_periode = %(period_id)s
and checkpoint_periode = %(period_id)s
and checkpoint_id = %(checkpoint_id)s
and rechnung_periode = %(period_id)s
%(umsatz_where)s
group by checkpoint_info, detail_artikel_text, detail_preis, detail_kellner, detail_gruppe %(table_code)s %(date)s
order by str_to_date(checkpoint_info, '%%d.%%m.%%Y'), detail_kellner %(date)s %(table_code)s , detail_artikel_text, detail_preis
		""" % {'period_id': self._getCurrentPeriodId(), 'checkpoint_id': cpId, 'umsatz_where': umsatzWhere, 'table_code': ', rechnung_tischCode' if self.ui.checkBox_showTableCode.isChecked() else '', 'date': ', detail_bonier_datum' if self.ui.checkBox_showDate.isChecked() else ''}
		
		return query
	
