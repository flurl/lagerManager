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
		
		self.setTableHeaders(['Datum', 'Kellner', 'Menge', 'Artikel', 'Preis', 'EK', 'EK total', 'Artikelgruppe', 'Tisch', 'Zeit'])
		
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
			purchasePrice = round(results.value(5).toFloat()[0], 2)
			purchasePriceTotal = round(results.value(6).toFloat()[0], 2)
			group = unicode(results.value(7).toString())
			
			index = 8
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
			data.append([date, waiter, amount, article, price, purchasePrice, purchasePriceTotal, group, table, time])
		
		self.setData(data)
		self.process()
		
	
		
	def mkQuery(self):
		"""return the query"""
		
		umsatzWhere = ""
		if self.ui.radioButton_umsatz.isChecked():
			umsatzWhere = " and tisch_bondetail_istUmsatz = 1 "
		elif self.ui.radioButton_aufwand.isChecked():
			umsatzWhere = " and tisch_bondetail_istUmsatz = 0 "
			
		cpId = self.ui.comboBox_checkpoint.itemData(self.ui.comboBox_checkpoint.currentIndex()).toInt()[0]
		
		query = """
select checkpoint_info, 
kellner_kurzName,
sum(tisch_bondetail_absmenge),
tisch_bondetail_text,
tisch_bondetail_preis,
getPurchasePrice(tisch_bondetail_text, tisch_bondetail_periode, NULL), 
sum(tisch_bondetail_absmenge*getPurchasePrice(tisch_bondetail_text, tisch_bondetail_periode, NULL)),
journal_gruppe
%(table_code)s %(date)s
from tische_aktiv left outer join rechnungen_basis
  on tisch_rechnung = rechnung_id,
journal_checkpoints as a, tische_bons, tische_bondetails, kellner_basis, tische_bereiche
where 1=1
and tischbereich_id = tisch_bereich
and tischbereich_periode = %(period_id)s
and kellner_id = tisch_bon_kellner
and kellner_periode = %(period_id)s
and checkpoint_id = %(checkpoint_id)s
and checkpoint_periode = %(period_id)s
and tische_aktiv.checkpoint_tag = checkpoint_id
and (rechnung_periode = %(period_id)s or rechnung_periode is null)
and tisch_periode = %(period_id)s
and tisch_bon_tisch = tisch_id
and tisch_bon_periode = %(period_id)s
and tisch_bondetail_bon = tisch_bon_id
and tisch_bondetail_periode = %(period_id)s
and checkpoint_typ = 1
%(umsatz_where)s
group by checkpoint_info, kellner_kurzName, tisch_bondetail_text, tisch_bondetail_preis, getPurchasePrice(tisch_bondetail_text, tisch_bondetail_periode, NULL), journal_gruppe %(table_code)s %(date)s
""" % {'period_id': self._getCurrentPeriodId(), 'checkpoint_id': cpId, 'umsatz_where': umsatzWhere, 'table_code': ',concat(tischbereich_kurzName , \'-\', tisch_pri_nummer ) ' if self.ui.checkBox_showTableCode.isChecked() else '', 'date': ', tisch_bon_dt_erstellung' if self.ui.checkBox_showDate.isChecked() else ''}
		
		return query
	
