# -*- coding: utf-8 -*-
import time
import copy

#from ui.reports.gesamteLieferungenReport_gui import Ui_GesamteLieferungenReport
from PyQt4 import QtCore, QtGui, QtSql

from textReport import TextReport



class RechnungenStatistikReport(TextReport):
    
    #uiClass = Ui_GesamteLieferungenReport
    ident = 'RechnungenStatistik'
    
    def __init__(self, parent=None):
        TextReport.__init__(self, parent)
                
        self.setHeader('Rechnungen Statistik')
        self.setFooter('here could be a nice footer')
        self.setTableHeaders([u'Ø Details', u'Ø Positionen', u'Ø Summe', 'Anzahl', 'Gesamt', 'Bar', 'Datum'])
        
        self.updateData()
        #self.process()
        

    def updateData(self):
        self.setData(self.mkQuery())
        self.process()
        
        
    
        
    def mkQuery(self):
        """return the query"""
        
        query = """
                select avg(c*1.0) as 'average detail count', 
				avg(sabs*1.0) as 'average position count', 
				avg(a) as 'average invoice sum', 
				count(distinct rechnung_id) as 'invoice count',
				sum(a) as 'total sum',
				rechnung_kellnerKurzName, cpi
				from 
				(select count(*) as c, sum(rechnung_detail_absmenge*rechnung_detail_preis) as a,
				sum(rechnung_detail_absmenge) as sabs,
				rechnung_id, rechnung_kellnerKurzName, checkpoint_info as cpi
				from rechnungen_details as ou, rechnungen_basis, journal_checkpoints
				where 1=1
				and rechnung_id = rechnung_detail_rechnung
				and checkpoint_tag = checkpoint_id
				and rechnung_tischbereich = 'THEKE BAR'
				and checkpoint_periode = %(period_id)s
				and rechnung_periode = %(period_id)s
				and rechnung_detail_periode = %(period_id)s
				group by rechnung_kellnerKurzName, checkpoint_info, rechnung_id) as t
				group by rechnung_kellnerKurzName, cpi
				order by str_to_date(cpi, '%%d.%%m.%%Y'), rechnung_kellnerKurzName
				""" % {'period_id': self._getCurrentPeriodId()}
        
        return query
    
