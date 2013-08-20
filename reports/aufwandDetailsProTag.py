# -*- coding: utf-8 -*-
import time
import copy
import datetime

from PyQt4 import QtCore, QtGui, QtSql

from textReport import TextReport
from ui.reports.aufwandDetailsProTag_gui import Ui_AufwandDetailsProTagReport


class AufwandDetailsProTagReport(TextReport):
	uiClass = Ui_AufwandDetailsProTagReport
	
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
			data.append([checkpoint, article, amount, sum_, tax, table])
		
		
		
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
			
			articleId = self.getArticleIdByName(article)
			avgPurchasePrice = self.getAveragePurchasePrice(articleId)
			purchasePrice = round(avgPurchasePrice*amount, 2)
			#purchasePrice = avgPurchasePrice
			
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
				select checkpoint_info, detail_artikel_text, sum(detail_absmenge), sum(detail_absmenge*detail_preis), detail_mwst, rechnung_tischBereich
from journal_details, journal_daten, journal_checkpoints, rechnungen_basis
where 1=1
and {0}
and daten_rechnung_id = rechnung_id
and detail_journal = daten_rechnung_id
and daten_checkpoint_tag = checkpoint_id
and detail_periode = {1}
and rechnung_periode = {2}
group by checkpoint_info, rechnung_tischBereich, detail_artikel_text, detail_istUmsatz, detail_mwst
order by str_to_date(checkpoint_info, '%d.%m.%Y') desc, detail_artikel_text
		""" 
		
		if not self.ui.checkBox_zeroBonierungen.isChecked():
			whereClause = "detail_istUmsatz = 0"
		else:
			whereClause = "(detail_istUmsatz = 0 or detail_preis = 0.0)"
		
		query = query.format(whereClause, self._getCurrentPeriodId(), self._getCurrentPeriodId())
		print query
		return query
	
	
	def getAveragePurchasePrice(self, articleId):
		perId = self._getCurrentPeriodId()
		
		periodArticles = {}
		try:
			periodArticles = self.__avgPriceCache[perId]
		except KeyError:
			self.__avgPriceCache[perId] = {}
		
		if articleId in periodArticles:
			return periodArticles[articleId]
		
		pStart, pEnd = self._getCurrentPeriodStartEnd()
		
		query = QtSql.QSqlQuery()
		query.prepare("""
						select count(*) 
						from lager_artikel 
						where 1=1
						and lager_artikel_artikel = ?
						and lager_artikel_periode = ?
						""")
		query.addBindValue(articleId)
		query.addBindValue(perId)
		query.exec_()
		if query.lastError().isValid():
			print 'Error selecting lager_artikel for article %s:' % articleId, query.lastError().text()
			return 0.0
		query.next()
		
		if query.value(0).toInt()[0] > 0:
			query = QtSql.QSqlQuery()
			query.prepare("""select round(sum(anzahl*einkaufspreis)/sum(anzahl), 2)
						from artikel_basis, lieferungen_details, lieferungen, lager_artikel, lager_einheiten
						where 1=1 
						and artikel_basis.artikel_id = lieferungen_details.artikel_id 
						and lieferungen_details.lieferung_id = lieferungen.lieferung_id
						and lager_artikel.lager_artikel_artikel = artikel_basis.artikel_id
						and lager_einheit_id = lager_artikel_einheit
						and lieferungen.datum between ? and ?
						and lager_artikel_periode = ?
						and lager_einheit_periode = ?
						and artikel_basis.artikel_periode = ?
						and find_in_set(artikel_basis.artikel_id, getCocktailArticleIds(?, ?)) > 0
						""")
						
			query.addBindValue(pStart.strftime('%Y-%m-%d %H:%M:%S'))
			query.addBindValue(pEnd.strftime('%Y-%m-%d %H:%M:%S'))
			query.addBindValue(perId)
			query.addBindValue(perId)
			query.addBindValue(perId)
			query.addBindValue(articleId)
			query.addBindValue(perId)
			
		else:
			query = QtSql.QSqlQuery()
			query.prepare("""
							select round(sum(anzahl*(einkaufspreis*(zutate_menge/lager_einheit_multiplizierer)))/sum(anzahl), 2)
							from artikel_basis as ab1, artikel_basis as ab2, lieferungen_details, lieferungen, lager_artikel, lager_einheiten, artikel_zutaten
							where 1=1 
							and lager_artikel_artikel = zutate_artikel
							and zutate_artikel = ab2.artikel_id
							and zutate_master_artikel = ab1.artikel_id
							and find_in_set(lieferungen_details.artikel_id, getCocktailArticleIds(ab2.artikel_id, ?)) > 0
							and lieferungen_details.lieferung_id = lieferungen.lieferung_id
							and lager_einheit_id = lager_artikel_einheit
							and lie_ist_verbrauch = 0
							and lieferungen.datum between ? and ?
							and lager_artikel_periode = ?
							and lager_einheit_periode = ?
							and ab1.artikel_periode = ?
							and ab2.artikel_periode = ?
							and zutate_periode = ?
							and ab1.artikel_id = ?
						""")
						
			#and ab2.artikel_id = lieferungen_details.artikel_id 
			query.addBindValue(perId)
			query.addBindValue(pStart.strftime('%Y-%m-%d %H:%M:%S'))
			query.addBindValue(pEnd.strftime('%Y-%m-%d %H:%M:%S'))
			query.addBindValue(perId)
			query.addBindValue(perId)
			query.addBindValue(perId)
			query.addBindValue(perId)
			query.addBindValue(perId)
			query.addBindValue(articleId)
			#query.addBindValue(perId)
		
		query.exec_()
		if query.lastError().isValid():
			print 'Error selecting average purchase price for article %s:' % articleId, query.lastError().text()
			return 0.0
		
		query.next()
		avgPrice = query.value(0).toFloat()[0]
		
		#no average price found? 
		#we use the purchase price from the wiffzach artikel_basis table
		if avgPrice - 0.001 <= 0:
			query = QtSql.QSqlQuery()
			query.prepare("""select artikel_ep from artikel_basis where artikel_id = ? and artikel_periode = ?""")
			query.addBindValue(articleId)
			query.addBindValue(perId)
			query.exec_()
			if query.lastError().isValid():
				print 'Error selecting purchase price from artikel_basis for article %s:' % articleId, query.lastError().text()
				return 0.0
			
			query.next()
			avgPrice = query.value(0).toFloat()[0]
		
		periodArticles[articleId] = avgPrice
		
		return avgPrice
	
	
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
		