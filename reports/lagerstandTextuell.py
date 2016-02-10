# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from inventur import InventurReport
from ui.reports.lagerstandTextuellReport_gui import Ui_LagerstandTextuellReport


class LagerstandTextuellReport(InventurReport):
    uiClass = Ui_LagerstandTextuellReport
    ident = 'LagerstandTextuell'
    
    def __init__(self, parent=None):
        InventurReport.__init__(self, parent)
                
        self.setHeader('Lagerstand')
        self.setFooter('here could be a nice footer')
        
        #self.updateData()
        
    def setupSignals(self):
        super(LagerstandTextuellReport, self).setupSignals()
        
        self.connect(self.ui.checkBox_useTillDate, QtCore.SIGNAL('stateChanged(int)'), self.updateData)
        self.connect(self.ui.checkBox_purchasePrice, QtCore.SIGNAL('stateChanged(int)'), self.updateData)
        
        
    def mkConsQuery(self):
        """returns the query for the consumption"""
        
        dateWhere = ""
        if self.ui.checkBox_useTillDate.isChecked():
            dateWhere = " and str_to_date(checkpoint_info, '%%d.%%m.%%Y') <= '%s' " % (self.ui.dateEdit_till.date().toPyDate().isoformat(), )
        
        query = """
                select checkpoint_id, checkpoint_info, art2.artikel_bezeichnung, sum(tisch_bondetail_absmenge*zutate_menge/lager_einheit_multiplizierer), count(*)
				from artikel_basis as art1, artikel_basis as art2
				left outer join artikel_basis as ept on art2.artikel_id = ept.artikel_id,
				artikel_zutaten, tische_aktiv, tische_bons, tische_bondetails, journal_checkpoints, lager_artikel, lager_einheiten
				where 1=1
				and lager_artikel_artikel = art2.artikel_id
				and tisch_bondetail_artikel = art1.artikel_id
				and zutate_master_artikel = art1.artikel_id
				and zutate_istRezept = 1
				and zutate_artikel = art2.artikel_id
				and tisch_bondetail_bon = tisch_bon_id
				and tisch_bon_tisch = tisch_id
				and checkpoint_tag = checkpoint_id
				and lager_artikel_einheit = lager_einheit_id
				and checkpoint_typ = 1
				and tisch_periode = %(period_id)s
				and tisch_bon_periode = %(period_id)s
				and tisch_bondetail_periode = %(period_id)s
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
                select checkpoint_id, checkpoint_info, a.artikel_bezeichnung, sum(tisch_bondetail_absmenge), count(*)
				from artikel_basis as a
				left outer join artikel_zutaten
				on zutate_master_artikel = artikel_id
				join tische_bondetails
				on tisch_bondetail_artikel = a.artikel_id
				left outer join artikel_basis as ept on tisch_bondetail_artikel = ept.artikel_id,
				journal_checkpoints, tische_aktiv, tische_bons
				where 1=1
				and zutate_istRezept is null
				and tisch_id = tisch_bon_tisch
				and tisch_bondetail_bon = tisch_bon_id
				and checkpoint_tag = checkpoint_id
				and checkpoint_typ = 1
				and tisch_periode = %(period_id)s
				and tisch_bon_periode = %(period_id)s
				and tisch_bondetail_periode = %(period_id)s
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
        if self.ui.checkBox_useTillDate.isChecked() and not self.ui.checkBox_purchasePrice.isChecked():
            maxDate = self.ui.dateEdit_till.date().toPyDate()
        return super(LagerstandTextuellReport, self).getPurchasePrice(artikelBez, maxDate)
    
    #def mkValueQuery(self):
        #date = None
        #if self.ui.checkBox_useTillDate.isChecked():
            #date = self.ui.dateEdit_till.date().toPyDate()
        #return super(LagerstandTextuellReport, self).mkValueQuery(date)