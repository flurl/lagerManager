# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.durchschnittUmsatzProTagReport_gui import Ui_DurchschnittUmsatzProTag
from textReport import TextReport



class DurchschnittUmsatzProTagReport(TextReport):
    
    uiClass = Ui_DurchschnittUmsatzProTag
    ident = 'durchschnittUmsatzProTag'
    
    def __init__(self, parent=None):
        TextReport.__init__(self, parent)
                
        self.setHeader('Durchschnittlicher Umsatz pro Wochentag')
        self.setFooter('here could be a nice footer')
        
        #self.updateData()
        self.updateData()
        self.process()
        
    def updateData(self):
        self.setData(self.mkQuery())
        
    
        
    def mkQuery(self):
        """return the query"""
        query = """
                select date_format(str_to_date(checkpoint_info, '%d.%m.%Y'), "%W") as Wochentag, 
HOUR(detail_bonier_datum),
round(sum(detail_absmenge*detail_preis)/(select count(*) from journal_checkpoints as b where date_format(str_to_date(a.checkpoint_info, '%d.%m.%Y'), "%w") = date_format(str_to_date(b.checkpoint_info, '%d.%m.%Y'), "%w") and b.checkpoint_periode = {0}), 2) as Durchschnitt
from journal_details, journal_daten, journal_checkpoints as a
where 1=1
and daten_checkpoint_tag = checkpoint_id
and detail_journal = daten_rechnung_id
and checkpoint_typ = 1
and detail_istUmsatz = 1
and detail_periode = {0}
and daten_periode = {0}
and checkpoint_periode = {0}
group by date_format(str_to_date(checkpoint_info, '%d.%m.%Y'), "%W"), HOUR(detail_bonier_datum)
order by (date_format(str_to_date(checkpoint_info, '%d.%m.%Y'), "%w")-7)%7, detail_bonier_datum
        """
        
        query = query.format(self._getCurrentPeriodId())
        
        return query
    
