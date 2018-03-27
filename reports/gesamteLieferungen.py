# -*- coding: utf-8 -*-
import time
import copy

from ui.reports.gesamteLieferungenReport_gui import Ui_GesamteLieferungenReport
from PyQt4 import QtCore, QtGui, QtSql

from textReport import TextReport



class GesamteLieferungenReport(TextReport):
    
    uiClass = Ui_GesamteLieferungenReport
    ident = 'GesamteLieferungen'
    
    def __init__(self, parent=None):
        TextReport.__init__(self, parent)
                
        self.setHeader('Insgesamt gelieferte Artikel')
        self.setFooter('here could be a nice footer')
        self.setTableHeaders(['Datum', 'Artikel', 'Anzahl', 'Einheit', 'Warenwert', 'Warenwert Durchschnitt'])
        
        self.updateData()
        #self.process()
        
        
    def setupSignals(self):
        super(GesamteLieferungenReport, self).setupSignals()
        self.connect(self.ui.comboBox_reportType, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
        self.connect(self.ui.comboBox_what, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
        self.connect(self.ui.checkBox_groupByProvider, QtCore.SIGNAL('stateChanged(int)'), lambda i: self.updateHeaders() and self.updateData())
        
        
    def updateData(self):
        self.setData(self.mkQuery())
        self.process()
        
        
    def updateHeaders(self):
        if self.ui.checkBox_groupByProvider.isChecked():
            headers = ['Datum', 'Lieferand', 'Artikel', 'Anzahl', 'Einheit', 'Warenwert', 'Warenwert Durchschnitt']
        else:
            headers = ['Datum', 'Artikel', 'Anzahl', 'Einheit', 'Warenwert', 'Warenwert Durchschnitt']
        self.setTableHeaders(headers)
        return True
        
        
    
        
    def mkQuery(self):
        """return the query"""
        reportType = unicode(self.ui.comboBox_reportType.currentText())
        
        datePart = "YEAR(lieferungen.datum)"
        if reportType == u"Monatlich":
                    datePart = "MONTH(lieferungen.datum)"
                    
        verbrauch = 0
        if (unicode(self.ui.comboBox_what.currentText()) == u"Verbräuche"):
            verbrauch = 1
            
        providerGroupBy = ""
        if self.ui.checkBox_groupByProvider.isChecked():
            providerGroupBy = ", lieferant_name "
        
        begin, end = self._getCurrentPeriodStartEnd()
        perId = self._getCurrentPeriodId()
        query = """
                select %s %s, artikel_bezeichnung, round(sum(anzahl), 2), lager_einheit_name, round(sum(getPurchasePrice(artikel_bezeichnung, artikel_periode, NULL)*anzahl), 2), round(max(getPurchasePrice(artikel_bezeichnung, artikel_periode, NULL)), 2)
                from artikel_basis, lieferungen_details, lieferungen, lager_artikel, lager_einheiten, lieferanten
                where 1=1 
                and lieferungen.lieferant_id = lieferanten.lieferant_id
                and artikel_basis.artikel_id = lieferungen_details.artikel_id 
                and lieferungen_details.lieferung_id = lieferungen.lieferung_id
                and lager_artikel.lager_artikel_artikel = artikel_basis.artikel_id
                and lager_einheit_id = lager_artikel_einheit
                and lie_ist_verbrauch = %s
                and lieferungen.datum between '%s' and '%s'
                and lager_artikel_periode = %s
                and lager_einheit_periode = %s
                and artikel_basis.artikel_periode = %s
                group by artikel_bezeichnung, lager_einheit_name, %s %s
                order by 1, 2
        """ % (datePart, providerGroupBy, verbrauch, begin.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S'), perId, perId, perId, datePart, providerGroupBy)
        
        print query
        
        return query
    
