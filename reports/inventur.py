# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from textReport import TextReport



class InventurReport(TextReport):
	
	def __init__(self, parent=None):
		TextReport.__init__(self, parent)
				
		self.setHeader('Inventur')
		self.setFooter('here could be a nice footer')
		
		self.updateData()
		
		
	def updateData(self):
		articles = {}

		query =  self.mkInvQuery()
		results = self.db.exec_(query)
		print query
		while results.next():
			name = unicode(results.value(0).toString())
			amount = results.value(1).toFloat()[0]
			articles[name] = amount
			
		query = self.mkConsQuery()
		results = self.db.exec_(query)
		print query
		print results.lastError().databaseText()
		while results.next():
			ckpId = results.value(0).toInt()[0]
			ckpInfo = results.value(1).toString()
			article = unicode(results.value(2).toString())
			amount = results.value(3).toFloat()[0]
			count = results.value(4).toInt()[0]
			articles[article] = articles.get(article, 0.0) - amount
			
			
		query = self.mkDelQuery()
		results = self.db.exec_(query)
		print query
		print results.lastError().databaseText()
		while results.next():
			date = results.value(0).toDateTime().toPyDateTime()
			article = unicode(results.value(1).toString())
			amount = results.value(2).toFloat()[0]
			articles[article] = articles.get(article, 0.0) + amount
		
		
		query = self.mkValueQuery()
		results = self.db.exec_(query)
		print query
		print results.lastError().databaseText()
		values = {}
		while results.next():
			values[unicode(results.value(0).toString())] = results.value(1).toFloat()[0]		
		
		i = 0
		data = []
		for k in sorted(articles.keys()):
			data.append([k, articles[k], values.get(k, 0.0), values.get(k, 0.0)*articles[k]])
		
		self.setData(data)
		self.process()
		
		
	def mkInvQuery(self):
		"""returns the query for the inventory"""
		query = """
			select artikel_bezeichnung, sum(anzahl)
			from artikel_basis, lagerstand
			where 1=1
			and lagerstand.artikel_id = artikel_basis.artikel_id
			and artikel_periode = %(period_id)s
			and lagerstand.periode_id = %(period_id)s
			group by artikel_bezeichnung
		""" % {'period_id': self._getCurrentPeriodId()}
		
		return query
		
		
	def mkConsQuery(self):
		"""returns the query for the consumption"""
		
		query = """
				select checkpoint_id, checkpoint_info, art2.artikel_bezeichnung, sum(detail_absmenge*zutate_menge/lager_einheit_multiplizierer), count(*)
				from artikel_basis as art1, artikel_basis as art2
				left outer join artikel_basis as ept on art2.artikel_bezeichnung = ept.artikel_bezeichnung,
				artikel_zutaten, journal_details, journal_daten, journal_checkpoints, lager_artikel, lager_einheiten
				where 1=1
				and lager_artikel_artikel = art2.artikel_id
				and detail_artikel_text = art1.artikel_bezeichnung
				and zutate_master_artikel = art1.artikel_id
				and zutate_istRezept = 1
				and zutate_artikel = art2.artikel_id
				and detail_journal = daten_rechnung_id
				and daten_checkpoint_jahr = checkpoint_id
				and lager_artikel_einheit = lager_einheit_id
				and checkpoint_typ = 3
				and detail_periode = %(period_id)s
				and daten_periode = %(period_id)s
				and checkpoint_periode = %(period_id)s
				and zutate_periode = %(period_id)s
				and art1.artikel_periode = %(period_id)s
				and art2.artikel_periode = %(period_id)s
				and (ept.artikel_periode = %(period_id)s or ept.artikel_periode is null)
				and (lager_artikel_periode = %(period_id)s or lager_artikel_periode is null)
				and lager_einheit_periode = %(period_id)s
				group by checkpoint_id, checkpoint_info, art2.artikel_bezeichnung
				""" % {'period_id': self._getCurrentPeriodId()}
		query += " union all "
		
		query += """
				select checkpoint_id, checkpoint_info, a.artikel_bezeichnung, sum(detail_absmenge), count(*)
				from artikel_basis as a
				left outer join artikel_zutaten
				on zutate_master_artikel = artikel_id
				join journal_details
				on detail_artikel_text = a.artikel_bezeichnung
				left outer join artikel_basis as ept on detail_artikel_text = ept.artikel_bezeichnung,
				journal_daten, journal_checkpoints
				where 1=1
				and zutate_istRezept is null
				and detail_journal = daten_rechnung_id
				and daten_checkpoint_jahr = checkpoint_id
				and checkpoint_typ = 3
				and detail_periode = %(period_id)s
				and daten_periode = %(period_id)s
				and checkpoint_periode = %(period_id)s
				and (zutate_periode = %(period_id)s or zutate_periode is null)
				and a.artikel_periode = %(period_id)s
				and (ept.artikel_periode = %(period_id)s or ept.artikel_periode is null)
				group by checkpoint_id, checkpoint_info, a.artikel_bezeichnung
				order by 1
				""" % {'period_id': self._getCurrentPeriodId()}
		#print query
		return query
		
	def mkDelQuery(self):
		"""return the query for the deliveries"""
		query = """
				select datum, artikel_bezeichnung, sum(anzahl)
				from artikel_basis, lager_artikel, lieferungen, lieferungen_details, perioden
				where 1=1
				and lager_artikel.lager_artikel_artikel = artikel_basis.artikel_id
				and lager_artikel.lager_artikel_artikel = lieferungen_details.artikel_id
				and lieferungen.lieferung_id = lieferungen_details.lieferung_id
				and artikel_periode = %(period_id)s
				and lager_artikel_periode = %(period_id)s
				and perioden.periode_id = %(period_id)s
				and lieferungen.datum between periode_start and periode_ende
				group by datum, artikel_bezeichnung
		""" % {'period_id': self._getCurrentPeriodId()}
		
		return query
	
	
	def mkValueQuery(self):
		pStart, pEnd = self._getCurrentPeriodStartEnd()
		pId = self._getCurrentPeriodId()
		
		query = """select artikel_bezeichnung, sum(anzahl*einkaufspreis)/sum(anzahl) 
				from artikel_basis, lieferungen_details, lieferungen
				where 1=1 
				and lieferungen_details.lieferung_id = lieferungen.lieferung_id
				and lieferungen_details.artikel_id = artikel_basis.artikel_id  
				and lieferungen.datum between '{0}' and '{1}'
				and artikel_basis.artikel_periode = {2}
				group by artikel_bezeichnung"""
				
		query = query.format(pStart, pEnd, pId)
		
		return query