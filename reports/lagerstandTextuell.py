# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from inventur import InventurReport
from ui.reports.lagerstandTextuellReport_gui import Ui_LagerstandTextuellReport


class LagerstandTextuellReport(InventurReport):
    uiClass = Ui_LagerstandTextuellReport
    
    def __init__(self, parent=None):
        InventurReport.__init__(self, parent)
                
        self.setHeader('Lagerstand')
        self.setFooter('here could be a nice footer')
        
        #self.updateData()
        
    def setupSignals(self):
        super(LagerstandTextuellReport, self).setupSignals()
        
        self.connect(self.ui.checkBox_useTillDate, QtCore.SIGNAL('stateChanged(int)'), self.updateData)
        
        
    def mkConsQuery(self):
        """returns the query for the consumption"""
        
        dateWhere = ""
        if self.ui.checkBox_useTillDate.isChecked():
            dateWhere = " and str_to_date(checkpoint_info, '%%d.%%m.%%Y') <= '%s' " % (self.ui.dateEdit_till.date().toPyDate().isoformat(), )
        
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
                and daten_checkpoint_tag = checkpoint_id
                and lager_artikel_einheit = lager_einheit_id
                and checkpoint_typ = 1
                and detail_periode = %(period_id)s
                and daten_periode = %(period_id)s
                and checkpoint_periode = %(period_id)s
                and zutate_periode = %(period_id)s
                and art1.artikel_periode = %(period_id)s
                and art2.artikel_periode = %(period_id)s
                and (ept.artikel_periode = %(period_id)s or ept.artikel_periode is null)
                and (lager_artikel_periode = %(period_id)s or lager_artikel_periode is null)
                and lager_einheit_periode = %(period_id)s
                %(date_where)s
                group by checkpoint_id, checkpoint_info, art2.artikel_bezeichnung
                """ % {'period_id': self._getCurrentPeriodId(), 'date_where': dateWhere}
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
                and daten_checkpoint_tag = checkpoint_id
                and checkpoint_typ = 1
                and detail_periode = %(period_id)s
                and daten_periode = %(period_id)s
                and checkpoint_periode = %(period_id)s
                and (zutate_periode = %(period_id)s or zutate_periode is null)
                and a.artikel_periode = %(period_id)s
                and (ept.artikel_periode = %(period_id)s or ept.artikel_periode is null)
                %(date_where)s
                group by checkpoint_id, checkpoint_info, a.artikel_bezeichnung
                order by 1
                """ % {'period_id': self._getCurrentPeriodId(), 'date_where': dateWhere}
        #print query
        return query
            
            
    def mkDelQuery(self):
        date = None
        if self.ui.checkBox_useTillDate.isChecked():
            date = self.ui.dateEdit_till.date().toPyDate()
        return super(LagerstandTextuellReport, self).mkDelQuery(date)
    
    def getPurchasePrice(self, artikelBez, maxDate=None):
        if self.ui.checkBox_useTillDate.isChecked():
            maxDate = self.ui.dateEdit_till.date().toPyDate()
        return super(LagerstandTextuellReport, self).getPurchasePrice(artikelBez, maxDate)
    
    #def mkValueQuery(self):
        #date = None
        #if self.ui.checkBox_useTillDate.isChecked():
            #date = self.ui.dateEdit_till.date().toPyDate()
        #return super(LagerstandTextuellReport, self).mkValueQuery(date)