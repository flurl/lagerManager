# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.rezepturenReport_gui import Ui_RezepturenReport
from tableReport import TableReport



class RezepturenReport(TableReport):
    
    uiClass = Ui_RezepturenReport
    ident = 'rezepturen'
    
    def __init__(self, parent=None):
        TableReport.__init__(self, parent)
                
        self.setHeader('Rezepturen')
        self.setFooter('here could be a nice footer')
        
        self.setTableHeaders(['Artikel', 'Menge', 'Zutat', 'Multiplikator'])
        
        self.updateData()
        self.process()
        
    def setupUi(self):
        super(RezepturenReport, self).setupUi()
            
    def setupSignals(self):
        super(RezepturenReport, self).setupSignals()
        #self.connect(self.ui.checkBox_withoutRecipe, QtCore.SIGNAL('toggled(bool)'), self.updateData)
        self.connect(self.ui.comboBox_what, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
        #self.connect(self.ui.radioButton_aufwand, QtCore.SIGNAL('toggled(bool)'), lambda checked: checked and self.updateData())
        #self.connect(self.ui.radioButton_umsatz, QtCore.SIGNAL('toggled(bool)'), lambda checked: checked and self.updateData())
        #self.connect(self.ui.radioButton_all, QtCore.SIGNAL('toggled(bool)'), lambda checked: checked and self.updateData())
        #self.connect(self.ui.checkBox_showDate, QtCore.SIGNAL('toggled(bool)'), self.updateData)
        
    def updateData(self):
        self.setData(self.mkQuery())
        self.process()
        #data = []

        #query =  self.mkQuery()
        #print query
        #results = self.db.exec_(query)
        
        #lastDate = None
        
        #while results.next():
            #date = unicode(results.value(0).toString())
            #waiter = unicode(results.value(1).toString())
            #amount = round(results.value(2).toFloat()[0], 2)
            #article = unicode(results.value(3).toString())
            #price = round(results.value(4).toFloat()[0], 2)
            #group = unicode(results.value(5).toString())
            
            #index = 6
            #if self.ui.checkBox_showTableCode.isChecked():
                #table = unicode(results.value(index).toString())
                #index += 1
            #else:
                #table = u''
            
            #if self.ui.checkBox_showDate.isChecked():
                #time = unicode(results.value(index).toString())
                #index += 1
            #else:
                #time = u''
            
            #if lastDate != date and lastDate is not None:
                #data.append([None])
                #lastDate = date
            #data.append([date, waiter, amount, article, price, group, table, time])
        
        #self.setData(data)
        #self.process()
        
    
        
    def mkQuery(self):
        """return the query"""
        
        if self.ui.comboBox_what.currentIndex() == 0:
            query = """
                    select art1.artikel_bezeichnung, zutate_menge, art2.artikel_bezeichnung, lager_einheit_multiplizierer
    from (artikel_basis as art1, artikel_basis as art2, artikel_zutaten)
    left outer join lager_artikel on lager_artikel_artikel = art2.artikel_id
    left outer join lager_einheiten on lager_artikel_einheit = lager_einheit_id
    where 1=1
    and zutate_master_artikel = art1.artikel_id
    and zutate_artikel = art2.artikel_id
    and zutate_istRezept = 1
    and art1.artikel_periode = %(period_id)s
    and art2.artikel_periode = %(period_id)s
    and zutate_periode = %(period_id)s
    and (lager_artikel_periode = %(period_id)s or lager_artikel_periode is null)
    and (lager_einheit_periode = %(period_id)s or lager_einheit_periode is null)
    order by art1.artikel_bezeichnung
            """ % {'period_id': self._getCurrentPeriodId()}
        
        elif self.ui.comboBox_what.currentIndex() == 1:
            query = """select art1.artikel_bezeichnung
    from artikel_basis as art1 
    left outer join artikel_zutaten on zutate_master_artikel = art1.artikel_id
    left outer join lager_artikel on lager_artikel_artikel = art1.artikel_id
    where 1=1
    and zutate_master_artikel is null
    and lager_artikel_lagerartikel is null
    and art1.artikel_periode = %(period_id)s
    and (zutate_periode = %(period_id)s or zutate_periode is null)
    and (lager_artikel_periode = %(period_id)s or lager_artikel_periode is null)
    order by art1.artikel_bezeichnung
            """ % {'period_id': self._getCurrentPeriodId()}
            
        elif self.ui.comboBox_what.currentIndex() == 2:
            query = """select art1.artikel_bezeichnung, zutate_menge, art2.artikel_bezeichnung
    from artikel_basis as art1, artikel_basis as art2, artikel_zutaten
    left outer join lager_artikel on lager_artikel_artikel = zutate_artikel
    where 1=1
    and art1.artikel_id = zutate_master_artikel
    and art2.artikel_id = zutate_artikel
    and lager_artikel_lagerartikel is null
    and zutate_istRezept = 1
    and art1.artikel_periode = %(period_id)s
    and art2.artikel_periode = %(period_id)s
    and zutate_periode = %(period_id)s
            """ % {'period_id': self._getCurrentPeriodId()}
        
        return query
    
