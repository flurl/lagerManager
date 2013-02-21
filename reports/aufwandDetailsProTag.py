# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from textReport import TextReport



class AufwandDetailsProTagReport(TextReport):
	
	def __init__(self, parent=None):
		TextReport.__init__(self, parent)
				
		self.setHeader('Aufwandbonierungendetails pro Tag')
		self.setFooter('here could be a nice footer')
		
		self.updateData()
		self.process()
		
	def updateData(self):
		data = []

		query =  self.mkQuery()
		results = self.db.exec_(query)
		lastCheckpoint = ''
		total = 0.0
		while results.next():
			checkpoint = unicode(results.value(0).toString())
			if checkpoint != lastCheckpoint and lastCheckpoint != '':
				data.append([lastCheckpoint, '', 'Total:', total])
				data.append(['-'*10, '-'*10, '-'*10, '-'*10])
				total = 0.0
			lastCheckpoint = checkpoint
			article = unicode(results.value(1).toString())
			amount = results.value(2).toFloat()[0]
			sum_ = round(results.value(3).toFloat()[0], 2)
			total += sum_
			data.append([checkpoint, article, amount, sum_])
		data.append([lastCheckpoint, '', 'Total:', total])
		
		self.setData(data)
		
	
		
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
	
