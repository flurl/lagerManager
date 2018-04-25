# -*- coding: utf-8 -*-
import time
import copy
import datetime

from PyQt4 import QtCore, QtGui, QtSql

from textReport import TextReport
from ui.reports.aufwandDetailsProTag_gui import Ui_AufwandDetailsProTagReport


class AufwandDetailsProTagReport(TextReport):
	uiClass = Ui_AufwandDetailsProTagReport
	ident = 'aufwandDetailsProTag'
	
	def __init__(self, parent=None):
		TextReport.__init__(self, parent)
		
		self.__avgPriceCache = {}
		self.__articleNameToIdCache = {}
				
		self.setHeader('Aufwandbonierungendetails pro Tag')
		self.setFooter('here could be a nice footer')
		self.setTableHeaders(['Checkpoint', 'Artikel', 'Anzahl', 'Summe brutto', 'Summe EK netto', 'VK MWSt.', 'Aufwandbreich'])
		self.setTableHeadersRepeat(True)
		
		self.updateData()
		self.process()
		
	def setupUi(self):
		super(AufwandDetailsProTagReport, self).setupUi()
		
		self.connect(self.ui.lineEdit_filterArticles, QtCore.SIGNAL('editingFinished ()'), self.onArticleFilterChanged)
		self.connect(self.ui.dateEdit_from, QtCore.SIGNAL('const QDate&'), self.onArticleFilterChanged)
		self.connect(self.ui.dateEdit_till, QtCore.SIGNAL('const QDate&'), self.onArticleFilterChanged)
		self.connect(self.ui.checkBox_zeroBonierungen, QtCore.SIGNAL('stateChanged (int)'), self.onZeroBonierungenChanged)
		
	def updateData(self):
		data = []

		query =  self.mkQuery()
		results = self.db.exec_(query)
		while results.next():
			checkpoint = unicode(results.value(0).toString())
			article = unicode(results.value(1).toString())
			amount = results.value(2).toFloat()[0]
			sum_ = round(results.value(3).toFloat()[0], 2)
			tax = round(results.value(4).toFloat()[0], 2)
			table = unicode(results.value(5).toString())
			purchasePrice = round(results.value(6).toFloat()[0], 2)
			data.append([checkpoint, article, amount, sum_, tax, table, purchasePrice])
		
		
		
		self.data = data
		self.setData(self.prepareData(data))
		
		pStart, pEnd = self._getCurrentPeriodStartEnd()
		
		self.ui.dateEdit_from.setDate(pStart)
		self.ui.dateEdit_till.setDate(pEnd)
		
	def prepareData(self, origData):
		data = []
		lastCheckpoint = ''
		checkpointTotal = 0.0
		checkpointTotalCount = 0.0
		total = 0.0
		totalCount = 0.0
		checkpointPurchasePriceTotal = 0.0
		totalPurchasePrice = 0.0
		for row in origData:
			checkpoint = row[0]
			if checkpoint is None:
				continue
			if checkpoint != lastCheckpoint and lastCheckpoint != '':
				data.append([[lastCheckpoint, 'strong'], ['Total:', 'strong'], [checkpointTotalCount, 'strong'], [checkpointTotal, 'strong'], [checkpointPurchasePriceTotal, 'strong'], '', ''])
				data.append([None, None, None, None, None, None, None])
				checkpointTotal = 0.0
				checkpointTotalCount = 0.0
				checkpointPurchasePriceTotal = 0.0
			lastCheckpoint = checkpoint
			article = row[1]
			amount = row[2]
			sum_ = row[3]
			tax = row[4]
			table = row[5]
			avgPurchasePrice = row[6]
			
			articleId = self.getArticleIdByName(article)
			purchasePrice = round(avgPurchasePrice*amount, 2)
			
			checkpointTotal += sum_
			checkpointTotalCount += amount
			checkpointPurchasePriceTotal += purchasePrice
			total += sum_
			totalCount += amount
			totalPurchasePrice += purchasePrice
			data.append([checkpoint, article, amount, sum_, purchasePrice, tax, table])
		
		data.append([lastCheckpoint, 'Total:', checkpointTotalCount, checkpointTotal, checkpointPurchasePriceTotal])
		data.append([None, None, None, None, None, None, None])
		data.append([['Alle Checkpoints:', 'strong'], '', [totalCount, 'strong'], [total, 'strong'], [totalPurchasePrice, 'strong'], '', ''])
		
		return data
		
		
	def onArticleFilterChanged(self):
		newText = self.ui.lineEdit_filterArticles.text()
		fromDate = self.ui.dateEdit_from.date().toPyDate()
		endDate = self.ui.dateEdit_till.date().toPyDate()
		
		data = [row for row in self.data if unicode(newText).lower() in unicode(row[1]).lower()]
		
		tmpData = []
		for row in data:
			try:
				chkPoint = datetime.datetime.strptime(row[0], '%d.%m.%Y').date()
			except (ValueError, TypeError):
				tmpData.append(row)
			if fromDate <= chkPoint <= endDate:
				tmpData.append(row)
		
		data = self.prepareData(tmpData)
		
		self.setData(data)
		self.process()
		
	def updatePeriod(self, p):
		super(AufwandDetailsProTagReport, self).updatePeriod(p)
		
		self.onArticleFilterChanged()
		
	
	def onZeroBonierungenChanged(self, state):
		print "0bons changed"
		self.updateData()
		self.process()
	
		
	def mkQuery(self):
		"""returns the query"""
		query = """
				select checkpoint_info, tisch_bondetail_text, sum(tisch_bondetail_absmenge), sum(tisch_bondetail_absmenge*tisch_bondetail_preis), tisch_bondetail_mwst, concat(tischbereich_kurzName , \'-\', tisch_pri_nummer ), getPurchasePrice(tisch_bondetail_text, tisch_bondetail_periode, NULL)
from tische_bondetails, tische_bons, tische_aktiv, journal_checkpoints, tische_bereiche
where 1=1
and {where}
and tischbereich_id = tisch_bereich
and tisch_bondetail_bon = tisch_bon_id
and tisch_bon_tisch = tisch_id
and tische_aktiv.checkpoint_tag = checkpoint_id
and tischbereich_periode = {period_id}
and tisch_bondetail_periode = {period_id}
and tisch_bon_periode = {period_id}
and tisch_periode = {period_id}
and checkpoint_periode = {period_id}
group by checkpoint_info, concat(tischbereich_kurzName , \'-\', tisch_pri_nummer ), tisch_bondetail_text, tisch_bondetail_istUmsatz, tisch_bondetail_mwst, getPurchasePrice(tisch_bondetail_text, tisch_bondetail_periode, NULL)
order by str_to_date(checkpoint_info, '%d.%m.%Y') desc, tisch_bondetail_text
		""" 
		
		if not self.ui.checkBox_zeroBonierungen.isChecked():
			whereClause = "tisch_bondetail_istUmsatz = 0"
		else:
			whereClause = "(tisch_bondetail_istUmsatz = 0 or tisch_bondetail_preis = 0.0)"
		
		query = query.format(where = whereClause, period_id=self._getCurrentPeriodId())
		print query
		return query
	
	
	def getArticleIdByName(self, article):
		perId = self._getCurrentPeriodId()
		
		periodArticles = {}
		try:
			periodArticles = self.__articleNameToIdCache[perId]
		except KeyError:
			self.__articleNameToIdCache[perId] = {}
		
		if article in periodArticles:
			return periodArticles[article]
		
		query = QtSql.QSqlQuery()
		query.prepare("""
						select artikel_id 
						from artikel_basis 
						where 1=1
						and artikel_bezeichnung = ?
						and artikel_periode = ?
						""")
		
		query.addBindValue(article)
		query.addBindValue(perId)
		
		query.exec_()
		query.next()
		id_ = query.value(0).toInt()[0]
		
		periodArticles[article] = id_
		
		return id_
		
