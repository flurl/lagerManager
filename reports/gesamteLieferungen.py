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
		self.setTableHeaders(['Artikel', 'Anzahl', 'Einheit', 'Warenwert', 'Warenwert Durchschnitt'])
		
		self.updateData()
		self.process()
		
	def updateData(self):
		"""articles = {}

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
		
		self.setData(data)"""
		self.setData(self.mkQuery())
		
		
	
		
	def mkQuery(self):
		"""return the query"""
		begin, end = self._getCurrentPeriodStartEnd()
		perId = self._getCurrentPeriodId()
		query = """
				select artikel_bezeichnung, round(sum(anzahl), 2), lager_einheit_name, round(sum(anzahl*einkaufspreis), 2), round(sum(anzahl*einkaufspreis)/sum(anzahl), 2)
				from artikel_basis, lieferungen_details, lieferungen, lager_artikel, lager_einheiten
				where 1=1 
				and artikel_basis.artikel_id = lieferungen_details.artikel_id 
				and lieferungen_details.lieferung_id = lieferungen.lieferung_id
				and lager_artikel.lager_artikel_artikel = artikel_basis.artikel_id
				and lager_einheit_id = lager_artikel_einheit
				and lie_ist_verbrauch = 0
				and lieferungen.datum between '%s' and '%s'
				and lager_artikel_periode = %s
				and lager_einheit_periode = %s
				and artikel_basis.artikel_periode = %s
				group by artikel_bezeichnung, lager_einheit_name order by 1
		""" % (begin.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S'), perId, perId, perId)

		return query
	
