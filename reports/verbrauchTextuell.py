# -*- coding: utf-8 -*-
import time
import copy
import numbers

from PyQt4 import QtCore, QtGui, QtSql

#from lagerstandTextuell import LagerstandTextuellReport
from textReport import TextReport
from ui.reports.verbrauchTextuellReport_gui import Ui_VerbrauchTextuellReport


class VerbrauchTextuellReport(TextReport):
    uiClass = Ui_VerbrauchTextuellReport
    
    def __init__(self, parent=None):
        TextReport.__init__(self, parent)
                
        self.setHeader('Verbrauch')
        self.setFooter('here could be a nice footer')
       # self.setTableHeaders(['Artikel', 'Menge', 'EK', 'Warenwert'])
        
        self.updateData()
        
    def setupSignals(self):
        super(VerbrauchTextuellReport, self).setupSignals()
        
        self.connect(self.ui.checkBox_useTillDate, QtCore.SIGNAL('stateChanged(int)'), self.updateData)
        self.connect(self.ui.radioButton_aufwand, QtCore.SIGNAL('toggled(bool)'), lambda checked: checked and self.updateData())
        self.connect(self.ui.radioButton_umsatz, QtCore.SIGNAL('toggled(bool)'), lambda checked: checked and self.updateData())
        self.connect(self.ui.radioButton_all, QtCore.SIGNAL('toggled(bool)'), lambda checked: checked and self.updateData())
        self.connect(self.ui.checkBox_showTableCode, QtCore.SIGNAL('toggled(bool)'), self.updateData)
        
    #def setData(self, data):
        """since the dataset comes from the inventur report and only the consumption is considered - which is usually subtracted -
        we have to multiply the data with -1 to get positive values"""
        
        #for i, row in enumerate(data):
            #for j, cell in enumerate(row):
                #if isinstance(cell, numbers.Number):
                    #data[i][j] *= -1
                    
        #return super(VerbrauchTextuellReport, self).setData(data)
        
    def updateData(self):
        articles = {}
        query = self.mkConsQuery()
        results = self.db.exec_(query)
        print query
        print results.lastError().databaseText()
        while results.next():
            article = unicode(results.value(0).toString())
            amount = results.value(1).toFloat()[0]
            count = results.value(2).toInt()[0]
            tableCode = ''
            if self.ui.checkBox_showTableCode.isChecked():
                tableCode = unicode(results.value(3).toString())
            tmpArt = articles.get(article, {tableCode: 0.0}) 
            tmpArt[tableCode] = tmpArt.get(tableCode, 0.0) + amount
            articles[article] = tmpArt
        
        
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
            for tableCode in articles[k]:
                data.append([k, tableCode, round(articles[k][tableCode], 2), round(values.get(k, 0.0), 2), round(values.get(k, 0.0)*articles[k][tableCode], 2)])
        
        self.setData(data)
        self.process()
        
    def mkConsQuery(self):
        """returns the query for the consumption"""
        
        dateWhere = ""
        if self.ui.checkBox_useTillDate.isChecked():
            dateWhere = " and str_to_date(checkpoint_info, '%%d.%%m.%%Y') <= '%s' " % (self.ui.dateEdit_till.date().toPyDate().isoformat(), )
        
        umsatzWhere = ""
        if self.ui.radioButton_umsatz.isChecked():
            umsatzWhere = " and detail_istUmsatz = 1 "
        elif self.ui.radioButton_aufwand.isChecked():
            umsatzWhere = " and detail_istUmsatz = 0 "
        
        query = """
                select art2.artikel_bezeichnung, sum(detail_absmenge*zutate_menge/lager_einheit_multiplizierer), count(*) %(table_code)s
                from artikel_basis as art1, artikel_basis as art2
                left outer join artikel_basis as ept on art2.artikel_bezeichnung = ept.artikel_bezeichnung,
                artikel_zutaten, journal_details, journal_daten, journal_checkpoints, lager_artikel, lager_einheiten, rechnungen_basis
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
                and daten_rechnung_id = rechnung_id
                and rechnung_periode = %(period_id)s
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
                %(umsatz_where)s
                group by art2.artikel_bezeichnung %(table_code)s
                """ % {'period_id': self._getCurrentPeriodId(), 'date_where': dateWhere, 'umsatz_where': umsatzWhere, 'table_code': ', rechnung_tischCode' if self.ui.checkBox_showTableCode.isChecked() else ''}
        query += " union all "
        
        query += """
                select a.artikel_bezeichnung, sum(detail_absmenge), count(*) %(table_code)s
                from artikel_basis as a
                left outer join artikel_zutaten
                on zutate_master_artikel = artikel_id
                join journal_details
                on detail_artikel_text = a.artikel_bezeichnung
                left outer join artikel_basis as ept on detail_artikel_text = ept.artikel_bezeichnung,
                journal_daten, journal_checkpoints, rechnungen_basis
                where 1=1
                and zutate_istRezept is null
                and detail_journal = daten_rechnung_id
                and daten_checkpoint_tag = checkpoint_id
                and checkpoint_typ = 1
                and daten_rechnung_id = rechnung_id
                and rechnung_periode = %(period_id)s
                and detail_periode = %(period_id)s
                and daten_periode = %(period_id)s
                and checkpoint_periode = %(period_id)s
                and (zutate_periode = %(period_id)s or zutate_periode is null)
                and a.artikel_periode = %(period_id)s
                and (ept.artikel_periode = %(period_id)s or ept.artikel_periode is null)
                %(date_where)s
                %(umsatz_where)s
                group by a.artikel_bezeichnung %(table_code)s
                order by 1
                """ % {'period_id': self._getCurrentPeriodId(), 'date_where': dateWhere, 'umsatz_where': umsatzWhere, 'table_code': ', rechnung_tischCode' if self.ui.checkBox_showTableCode.isChecked() else ''}
        print query
        return query
    
    #def mkInvQuery(self):
    #    return ""
            
    #def mkDelQuery(self):
    #    return ""
    
    def mkValueQuery(self):
        pStart, pEnd = self._getCurrentPeriodStartEnd()
        pId = self._getCurrentPeriodId()
        
        dateWhere = ""
        if self.ui.checkBox_useTillDate.isChecked():
            date = self.ui.dateEdit_till.date().toPyDate()
            dateWhere = " and lieferungen.datum <= '%s' " % (maxDate.isoformat(), )
        
        query = """select artikel_bezeichnung, sum(anzahl*einkaufspreis)/sum(anzahl) 
                from artikel_basis, lieferungen_details, lieferungen
                where 1=1 
                and lieferungen_details.lieferung_id = lieferungen.lieferung_id
                and lieferungen_details.artikel_id = artikel_basis.artikel_id  
                and lieferungen.datum between '{0}' and '{1}'
                and artikel_basis.artikel_periode = {2}
                {3}
                group by artikel_bezeichnung"""
                
        query = query.format(pStart, pEnd, pId, dateWhere)
        
        return query