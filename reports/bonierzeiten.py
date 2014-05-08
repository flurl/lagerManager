# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from textReport import TextReport



class Bonierzeiten(TextReport):
	
	def __init__(self, parent=None):
		TextReport.__init__(self, parent)
				
		self.setHeader('Bonierzeiten')
		self.setFooter('here could be a nice footer')
		
		self.updateData()
		self.process()
		
	def updateData(self):
		query =  self.mkQuery()
		self.setData(query)
		
		
	
		
	def mkQuery(self):
		"""return the query"""
		query = """
				select checkpoint_id, checkpoint_info, detail_kellner, min(detail_bonier_datum), max(detail_bonier_datum), round(TIMESTAMPDIFF(SECOND,min(detail_bonier_datum),max(detail_bonier_datum))/3600, 2)
from journal_details, journal_daten, journal_checkpoints
where 1=1
and daten_checkpoint_tag = checkpoint_id
and detail_journal = daten_rechnung_id
and detail_periode = %s
group by checkpoint_id, checkpoint_info, detail_kellner
order by 1 desc, 3
		""" % self._getCurrentPeriodId()
		
		return query
	
