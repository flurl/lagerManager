# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from textReport import TextReport



class Bonierzeiten(TextReport):
    ident = 'Bonierzeiten'
    
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
                select checkpoint_id, checkpoint_info, kellner_kurzName, min(tisch_bon_dt_erstellung), max(tisch_bon_dt_erstellung), round(TIMESTAMPDIFF(SECOND,min(tisch_bon_dt_erstellung),max(tisch_bon_dt_erstellung))/3600, 2), round(sum(tisch_bondetail_absmenge*tisch_bondetail_preis), 2)
from journal_checkpoints, tische_aktiv, tische_bons, tische_bondetails, kellner_basis
where 1=1
and checkpoint_tag = checkpoint_id
and tisch_bon_tisch = tisch_id
and tisch_bon_kellner = kellner_id
and tisch_bondetail_bon = tisch_bon_id
and tisch_bondetail_istUmsatz = 1
and tisch_bondetail_periode = %(period_id)s
and tisch_bon_periode = %(period_id)s
and tisch_periode = %(period_id)s
and checkpoint_periode = %(period_id)s
and kellner_periode = %(period_id)s
group by checkpoint_id, checkpoint_info, kellner_kurzName
order by 1 desc, 3
        """ % {'period_id': self._getCurrentPeriodId()}
        #print query
        return query
    
