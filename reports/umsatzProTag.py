# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from textReport import TextReport



class UmsatzProTagReport(TextReport):
    ident = 'UmsatzProTag'
    
    def __init__(self, parent=None):
        TextReport.__init__(self, parent)
                
        self.setHeader('Umsatz pro Tag')
        self.setFooter('here could be a nice footer')
        
        #self.updateData()
        self.updateData()
        self.process()
        
    def updateData(self):
        self.setData(self.mkQuery())
        
    
        
    def mkQuery(self):
        """return the query"""
        query = """
                select checkpoint_info, detail_kellner,
round(sum(detail_absmenge*detail_preis), 2)
from journal_details, journal_daten, journal_checkpoints as a
where 1=1
and daten_checkpoint_tag = checkpoint_id
and detail_journal = daten_rechnung_id
and checkpoint_typ = 1
and detail_istUmsatz = 1
and detail_periode = {0}
and daten_periode = {0}
and checkpoint_periode = {0}
group by checkpoint_info, detail_kellner
order by str_to_date(checkpoint_info, '%d.%m.%Y'), detail_kellner
        """
        
        query = query.format(self._getCurrentPeriodId())
        
        return query
    
