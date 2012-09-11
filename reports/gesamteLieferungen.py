# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from textReport import TextReport



class GesamteLieferungenReport(TextReport):
	
	def __init__(self, parent=None):
		TextReport.__init__(self, parent)
				
		self.setHeader('Insgesamt gelieferte Artikel')
		self.setFooter('here could be a nice footer')
		
		self.updateData()
		self.process()
		
	def updateData(self):
		articles = {}

		query =  self.mkQuery()
		results = self.db.exec_(query)
		while results.next():
			name = unicode(results.value(0).toString())
			amount = results.value(1).toFloat()[0]
			articles[name] = amount
		
		i = 0
		data = []
		for k in sorted(articles.keys()):
			data.append([k, articles[k]])
		
		self.setData(data)
		
		
	
		
	def mkQuery(self):
		"""return the query"""
		query = """
				select artikel_bezeichnung, sum(anzahl) from artikel_basis, lieferungen_details where artikel_basis.artikel_id = lieferungen_details.artikel_id group by artikel_bezeichnung order by 1
		"""
		
		return query
	
