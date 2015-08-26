# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from textReport import TextReport



class NichtVorhandeneBonierteArtikelReport(TextReport):
    ident = 'NichtVorhandeneBonierteArtikel'
    
    def __init__(self, parent=None):
        TextReport.__init__(self, parent)
                
        self.setHeader('Bonierte aber nicht mehr vorhandene Artikel')
        self.setFooter('here could be a nice footer')
        #self.setTableHeaders(['Artikel', 'Anzahl', 'Einheit', 'Warenwert', 'Warenwert Durchschnitt'])
        
        self.updateData()
        self.process()
        
    def updateData(self):
        self.setData(self.mkQuery())
        
        
    
        
    def mkQuery(self):
        """return the query"""
        perId = self._getCurrentPeriodId()
        query = """
                select distinct detail_artikel_text 
                from journal_details 
                where 1=1
                and detail_periode = %s 
                and detail_artikel_text not in (select artikel_bezeichnung from artikel_basis where artikel_periode = %s)
        """ % (perId, perId)

        return query
    
