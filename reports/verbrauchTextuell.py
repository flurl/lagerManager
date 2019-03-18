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
    ident = 'VerbrauchTextuell'

    def __init__(self, parent=None):
        TextReport.__init__(self, parent)
        self.setHeader('Verbrauch')
        self.setFooter('here could be a nice footer')
        
        self.setTableHeaders(['Artikel', 'Tisch', 'Anzahl', 'EK', 'Summe EK netto'])
        self.setTableHeadersRepeat(True)
        
        self.updateData()

    def setupSignals(self):
        super(VerbrauchTextuellReport, self).setupSignals()

        self.connect(self.ui.checkBox_useTillDate, QtCore.SIGNAL('stateChanged(int)'), self.updateData)
        self.connect(self.ui.radioButton_aufwand, QtCore.SIGNAL('toggled(bool)'), lambda checked: checked and self.updateData())
        self.connect(self.ui.radioButton_umsatz, QtCore.SIGNAL('toggled(bool)'), lambda checked: checked and self.updateData())
        self.connect(self.ui.radioButton_all, QtCore.SIGNAL('toggled(bool)'), lambda checked: checked and self.updateData())
        self.connect(self.ui.checkBox_showTableCode, QtCore.SIGNAL('toggled(bool)'), self.updateData)
        self.connect(self.ui.checkBox_includeLMData, QtCore.SIGNAL('toggled(bool)'), self.updateData)

    def updateData(self):
        articles = {}
        query = self.mkConsQuery()
        results = self.db.exec_(query)
        print query
        #print results.lastError().databaseText()
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
        
        if self.ui.checkBox_includeLMData.isChecked():
            query = self.mkDelQuery()
            results = self.db.exec_(query)
            print query
            #print results.lastError().databaseText()
            while results.next():
                article = unicode(results.value(1).toString())
                amount = results.value(2).toFloat()[0]
                tableCode = ''
                if self.ui.checkBox_showTableCode.isChecked():
                    tableCode = u'LM'
                tmpArt = articles.get(article, {tableCode: 0.0}) 
                tmpArt[tableCode] = tmpArt.get(tableCode, 0.0) - amount #verbrauche are negative values in the db => minus
                articles[article] = tmpArt

        i = 0
        data = []
        for k in sorted(articles.keys()):
            purchasePrice = self.getPurchasePrice(k)
            for tableCode in articles[k]:
                data.append([k, tableCode, round(articles[k][tableCode], 2), round(purchasePrice, 2), round(purchasePrice*articles[k][tableCode], 2)])

        self.setData(data)
        self.process()

    def mkConsQuery(self):
        """returns the query for the consumption"""

        dateWhere = ""
        if self.ui.checkBox_useTillDate.isChecked():
            dateWhere = " and str_to_date(checkpoint_info, '%%d.%%m.%%Y') <= '%s' " % (self.ui.dateEdit_till.date().toPyDate().isoformat(), )

        umsatzWhere = ""
        if self.ui.radioButton_umsatz.isChecked():
            umsatzWhere = " and tisch_bondetail_istUmsatz = 1 "
        elif self.ui.radioButton_aufwand.isChecked():
            umsatzWhere = " and tisch_bondetail_istUmsatz = 0 "

        query = """
                select art2.artikel_bezeichnung, sum(tisch_bondetail_absmenge*zutate_menge/lager_einheit_multiplizierer), count(*) %(table_code)s
		        from artikel_basis as art1, artikel_basis as art2
		        left outer join artikel_basis as ept on art2.artikel_id = ept.artikel_id,
		        artikel_zutaten, tische_aktiv, tische_bons, tische_bondetails, journal_checkpoints, lager_artikel, lager_einheiten, tische_bereiche
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
		        and tisch_bereich = tischbereich_id
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
		        and tischbereich_periode = %(period_id)s
                %(date_where)s
                %(umsatz_where)s
                group by art2.artikel_bezeichnung %(table_code)s
                """ % {'period_id': self._getCurrentPeriodId(), 'date_where': dateWhere, 'umsatz_where': umsatzWhere, 'table_code': ', concat(tischbereich_kurzName, "-", tisch_pri_nummer)' if self.ui.checkBox_showTableCode.isChecked() else ''}
        query += " union all "
        
        query += """
                select a.artikel_bezeichnung, sum(tisch_bondetail_absmenge), count(*) %(table_code)s
		        from artikel_basis as a
		        left outer join artikel_zutaten
		        on zutate_master_artikel = artikel_id
		        join tische_bondetails
		        on tisch_bondetail_artikel = a.artikel_id
		        left outer join artikel_basis as ept on tisch_bondetail_artikel = ept.artikel_id,
		        journal_checkpoints, tische_aktiv, tische_bons, tische_bereiche
		        where 1=1
		        and zutate_istRezept is null
		        and tisch_id = tisch_bon_tisch
		        and tisch_bondetail_bon = tisch_bon_id
		        and checkpoint_tag = checkpoint_id
		        and tisch_bereich = tischbereich_id
		        and checkpoint_typ = 1
		        and tisch_periode = %(period_id)s
		        and tisch_bon_periode = %(period_id)s
		        and tisch_bondetail_periode = %(period_id)s
		        and checkpoint_periode = %(period_id)s
		        and (zutate_periode = %(period_id)s or zutate_periode is null)
		        and a.artikel_periode = %(period_id)s
		        and (ept.artikel_periode = %(period_id)s or ept.artikel_periode is null)
		        and tischbereich_periode = %(period_id)s
                %(date_where)s
                %(umsatz_where)s
                group by a.artikel_bezeichnung %(table_code)s
                order by 1
                """ % {'period_id': self._getCurrentPeriodId(), 'date_where': dateWhere, 'umsatz_where': umsatzWhere, 'table_code': ', concat(tischbereich_kurzName, "-", tisch_pri_nummer)' if self.ui.checkBox_showTableCode.isChecked() else ''}
        return query

    def mkDelQuery(self, maxDate=None):
        """return the query for the deliveries"""
        
        dateWhere = ""
        if maxDate is not None:
            dateWhere = " and lieferungen.datum <= '%s' " % (maxDate.isoformat(), )
        
        query = """
                select datum, artikel_bezeichnung, sum(anzahl)
                from artikel_basis, lager_artikel, lieferungen, lieferungen_details, perioden
                where 1=1
                and lager_artikel.lager_artikel_artikel = artikel_basis.artikel_id
                and lager_artikel.lager_artikel_artikel = lieferungen_details.artikel_id
                and lieferungen.lieferung_id = lieferungen_details.lieferung_id
                and lieferungen.lie_ist_verbrauch = 1
                and artikel_periode = %(period_id)s
                and lager_artikel_periode = %(period_id)s
                and perioden.periode_id = %(period_id)s
                and lieferungen.datum between periode_start and periode_ende
                %(date_where)s
                group by datum, artikel_bezeichnung
        """ % {'period_id': self._getCurrentPeriodId(), 'date_where': dateWhere}
        
        return query
