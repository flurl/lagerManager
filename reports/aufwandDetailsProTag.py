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
				
		self.setHeader('Aufwandbonierungendetails pro Tag')
		self.setFooter('here could be a nice footer')
		
		self.updateData()
		self.process()
		
	def setupUi(self):
		super(AufwandDetailsProTagReport, self).setupUi()
		
		self.connect(self.ui.lineEdit_filterArticles, QtCore.SIGNAL('editingFinished ()'), self.onArticleFilterChanged)
		self.connect(self.ui.dateEdit_from, QtCore.SIGNAL('const QDate&'), self.onArticleFilterChanged)
		self.connect(self.ui.dateEdit_till, QtCore.SIGNAL('const QDate&'), self.onArticleFilterChanged)
		
	def updateData(self):
		data = []

		query =  self.mkQuery()
		results = self.db.exec_(query)
		while results.next():
			checkpoint = unicode(results.value(0).toString())
			article = unicode(results.value(1).toString())
			amount = results.value(2).toFloat()[0]
			sum_ = round(results.value(3).toFloat()[0], 2)
			data.append([checkpoint, article, amount, sum_])
		
		
		
		self.data = data
		self.setData(self.prepareData(data))
		
	def prepareData(self, origData):
		data = []
		lastCheckpoint = ''
		checkpointTotal = 0.0
		checkpointTotalCount = 0.0
		total = 0.0
		totalCount = 0.0
		for row in origData:
			checkpoint = row[0]
			if checkpoint is None:
				continue
			if checkpoint != lastCheckpoint and lastCheckpoint != '':
				data.append([[lastCheckpoint, 'strong'], ['Total:', 'strong'], [checkpointTotalCount, 'strong'], [checkpointTotal, 'strong']])
				data.append([None, None, None, None])
				checkpointTotal = 0.0
				checkpointTotalCount = 0.0
			lastCheckpoint = checkpoint
			article = row[1]
			amount = row[2]
			sum_ = row[3]
			checkpointTotal += sum_
			checkpointTotalCount += amount
			total += sum_
			totalCount += amount
			data.append([checkpoint, article, amount, sum_])
		
		data.append([lastCheckpoint, 'Total:', checkpointTotalCount, checkpointTotal])
		data.append([None, None, None, None])
		data.append([['Alle Checkpoints:', 'strong'], '', [totalCount, 'strong'], [total, 'strong']])
		
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
		
		pStart, pEnd = self._getCurrentPeriodStartEnd()
		
		self.ui.dateEdit_from.setDate(pStart)
		self.ui.dateEdit_till.setDate(pEnd)
		
		self.onArticleFilterChanged()
	
		
	def mkQuery(self):
		"""returns the query"""
		query = """
				select checkpoint_info, detail_artikel_text, sum(detail_absmenge), sum(detail_absmenge*detail_preis)
from journal_details, journal_daten, journal_checkpoints
where 1=1
and detail_istUmsatz = 0
and detail_journal = daten_rechnung_id
and daten_checkpoint_tag = checkpoint_id
and detail_periode = %s
group by checkpoint_info, detail_artikel_text
order by str_to_date(checkpoint_info, '%%d.%%m.%%Y') desc, detail_artikel_text
		""" % (self._getCurrentPeriodId(), )
		
		return query
	
