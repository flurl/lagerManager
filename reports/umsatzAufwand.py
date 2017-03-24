# -*- coding: utf-8 -*-
import time
import datetime
import copy

from PyQt4 import QtCore, QtGui, QtSql


from graphicsReport import GraphicsReport



class UmsatzAufwandReport(GraphicsReport):
    ident = 'UmsatzAufwand'
    
    def __init__(self, parent=None):
        GraphicsReport.__init__(self, parent)
        
        dateFunc = lambda day: self.days[int(day)]
        percentFunc = lambda percent: unicode(round(float(percent), 2))+'%'
        formatter = [None, dateFunc, percentFunc]
        
        self.setDataFormatter(formatter)
        self.updateData()
        #self.plot()
                
    def updateData(self):
        dp = []
        extraData = []
        markingData = []
        self.days = []
        
        query =  self.mkUmsatzQuery()
        print query
        results = self.db.exec_(query)

        while results.next():
            date = unicode(results.value(0).toString())
            ratio = results.value(1).toFloat()[0]
            revenue = results.value(2).toFloat()[0]
            aufwand = results.value(3).toFloat()[0]
            dp.append({'ratio': ratio})
            extraData.append({'ratio': [revenue, aufwand]})
            markingData.append(date)
            self.days.append(date)

        #print dp
        self.dp = copy.deepcopy(dp)
        self.setDatapoints(copy.deepcopy(dp))
        self.setMarkingData(markingData)
        self.setExtraData(extraData)
        self.plot()
        
            
        
    def mkUmsatzQuery(self):
        query = """
select str_to_date(checkpoint_info, '%d.%m.%Y'), sum(case when tisch_bondetail_istUmsatz = 0 then tisch_bondetail_absmenge*tisch_bondetail_preis else 0 end)/sum(case when tisch_bondetail_istUmsatz = 1 then tisch_bondetail_absmenge*tisch_bondetail_preis else 0 end)*100 as ratio,
sum(case when tisch_bondetail_istUmsatz = 1 then tisch_bondetail_absmenge*tisch_bondetail_preis else 0 end) as revenue, sum(case when tisch_bondetail_istUmsatz = 0 then tisch_bondetail_absmenge*tisch_bondetail_preis else 0 end) as aufwand
from tische_bondetails, tische_bons, tische_aktiv, journal_checkpoints
where 1=1
and tisch_bondetail_bon = tisch_bon_id
and tisch_bon_tisch = tisch_id
and checkpoint_id = checkpoint_tag
and tisch_bondetail_periode = {period_id}
and tisch_bon_periode = {period_id}
and tisch_periode = {period_id}
and checkpoint_periode = {period_id}
group by checkpoint_info
order by 1
            """
            
        query = query.format(period_id=self._getCurrentPeriodId())
        
        return query
        
        
    
