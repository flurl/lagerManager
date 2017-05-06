# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from tableReport import TableReport



class UmsatzProTagReport(TableReport):
    ident = 'UmsatzProTag'
    
    def __init__(self, parent=None):
        TableReport.__init__(self, parent)
                
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
                select checkpoint_info, dayname(str_to_date(checkpoint_info, '%d.%m.%Y')), rechnung_kellnerkurzName,
round(sum(rechnung_detail_absmenge*rechnung_detail_preis), 2)
from rechnungen_details, rechnungen_basis, journal_checkpoints as a
where 1=1
and checkpoint_tag = checkpoint_id
and rechnung_detail_rechnung = rechnung_id
and checkpoint_typ = 1
and rechnung_tischBereich not in ('PERSONALVERBRAUCH', 'REPRAESENTATION', 'EIGENVERBRAUCH', 'VERDERB', 'GUTSCHEINE')
and rechnung_detail_periode = {0}
and rechnung_periode = {0}
and checkpoint_periode = {0}
group by checkpoint_info, rechnung_kellnerkurzName
order by str_to_date(checkpoint_info, '%d.%m.%Y'), rechnung_kellnerkurzName
        """
        
        query = query.format(self._getCurrentPeriodId())
        
        return query
    
