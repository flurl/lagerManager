# -*- coding: utf-8 -*-
from PyQt4 import QtCore

from lib import datetimehelper

from lib.LMDatabaseObject import LMDatabaseObject
from lib.LMDatabaseRelation import LMDatabaseRelation

#import lib.Gehalt

class Dienstnehmer(LMDatabaseObject):
    
    _DBTable = 'dienstnehmer'
    _dynamicColumns = {'din_stundensatz': 'getHourlyWage'}
    dienste = LMDatabaseRelation('lib.Dienst.Dienst', 'die_dinid')
    gehalt = LMDatabaseRelation('din_gehid', 'lib.Gehalt.Gehalt')
    beschaeftigungsbereich = LMDatabaseRelation('din_bebid', 'lib.Beschaeftigungsbereich.Beschaeftigungsbereich')
    
    def __init__(self, pk=None):
        super(Dienstnehmer, self).__init__(pk)
        
        
        
    def getRemainingSalary(self, date=None, excludeEventId=None):
        remainingSalary = self['din_gehalt']
        duties = self.getDuties(date, excludeEventId)
        for d in duties:
            earnings = d.getEarnings()
            remainingSalary -= d.getEarnings()
            
        print "BP3 remainingSalary for %s is %s" % (self['din_name'], remainingSalary)
        return remainingSalary
	
    
    def getDuties(self, date=None, excludeEventId=None, excludeDutyId = None):
        monthBegin, monthEnd = datetimehelper.getMonthBeginEnd(date)
        
        query = """select die_id
                from dienste, veranstaltungen
                where 1=1
                and die_dinid = ?
                and die_verid = ver_id
                and ver_datum between ? and ?"""
                
        if excludeEventId is not None: 
            query +=  " and die_verid != %s" % excludeEventId

        
        if excludeDutyId is not None:
            try:
                it = iter(excludeDutyId)
                ids = [str(id_) for id_ in excludeDutyId]
                if len(ids) > 0:
                    query += " and die_id not in (" + ",".join(ids) + ")"
            except TypeError as te:
                print te
                query += " and die_id != %s " % excludeDutyId
        
        values = [self['din_id'], QtCore.QDateTime(monthBegin), QtCore.QDateTime(monthEnd)]
        
        res = self.runQuery(query, values)
        
        duties = []
        while res.next():
            duties.append(lib.Dienst.Dienst(res.value(0).toInt()[0]))
            
        return duties
    
    
    def getHourlyWage(self, date=None):
        #hourly = self['gehalt']['stundensatz']
        hourly = self['gehalt'].getHourlyWage(date)
        return hourly
    
    
    def isAvailableForDate(self, date=None):
        if date is None:
            date = datetimehelper.now()
        date = QtCore.QDateTime(date)
        
        query = """select empIsAvailableForDate(?, ?)"""
        
        values = [self['din_id'], QtCore.QDateTime(date)]
        
        res = self.runQuery(query, values)
        res.next()
        retVal = res.value(0).toInt()[0]
        print "isAvailableForDate:", retVal
        return retVal
        
      
    def getTotals(self, forWhat, period):
    
        def getKey(d):
            d = d.toPyDateTime()
            if forWhat == 'monthly':
                return (d.year, d.month)
            else:
                return (d.isocalendar()[0], d.isocalendar()[1])
        
        period =period*-1
        enddate = datetimehelper.now()
        
        if forWhat == 'weekly':
            datefunc = datetimehelper.addWeeks
        elif forWhat == 'monthly':
            datefunc = datetimehelper.addMonths
        else:
            raise IncorrectPeriodException
        
        startDate = datefunc(enddate, period)
        print "startDate", startDate
        
        data = {}
        
        duties = []
        for i in range(abs(period)):
            duties += self.getDuties(datefunc(startDate, i), excludeDutyId=[d['die_id'] for d in duties])
        
        print 'duties:', len(duties)
            
        for d in duties:
            k = getKey(d['die_beginn'])
            total = data.get(k, {'count': 0, 'hours': 0.0, 'naz': 0})
            #print "bp1:",total
            data[k] = {'count': total['count']+1, 'hours': total['hours']+d.getWorkingHours(), 'naz': total['naz']+(1 if d.getNAZ()>0.0001 else 0)}
        print "bp2:",data
        return data
        

    def getAvg(self, forWhat, period):
        totals = self.getTotals(forWhat, period)
        numberOfDatapoints = 0
        countTotal = 0.0
        hoursTotal = 0.0
        nazTotal = 0.0
        for k, dp in totals.items():
            numberOfDatapoints += 1
            countTotal += dp['count']
            hoursTotal += dp['hours']
            nazTotal += dp['naz']
        
        if numberOfDatapoints == 0:
            return (0, 0, 0, 0)
        
        countAvg = countTotal/numberOfDatapoints
        hoursAvg = hoursTotal/numberOfDatapoints
        nazAvg = nazTotal/numberOfDatapoints
        
        print "countAvg:", countAvg, "hoursAvg:", hoursAvg
        return (numberOfDatapoints, countAvg, hoursAvg, nazAvg)
    
    
if __name__ == '__main__':
    import sys
    import DBConnection
    import lib.Dienst
    print sys.argv
    DBConnection.connect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    
    dbObj = Dienstnehmer()
    dbObj.get(22)
    print unicode(dbObj['din_name'])
    
    print (("*"*20)+'\n')*5
    
    while dbObj.next():
        print unicode(dbObj['din_name'])
    
    #dbObj.getTotals()
    #dbObj.getTotals('weekly', -13)
    #dbObj.getTotals('monthly', -12)
    #print "avg:", dbObj.getAvg('weekly', 1)
    #print "avg:", dbObj.getAvg('monthly', 3)
    
    
    """
    dbObj = Dienstnehmer()
    for dn in dbObj.find('din_bebid', 1):
        print unicode(dn['din_name'])
        
    dbObj.find('din_bebid', 2)
    while dbObj.next():
        print unicode(dbObj['din_name'])
    
    print (("*"*20)+'\n')*5
    print "finding dienste"
    dbObj.get(43)
    for d in dbObj['dienste']:
        print d['die_beginn']
    
    
    print (("*"*20)+'\n')*5
    
    dbObj = lib.Dienst.Dienst()
    dbObj.get(180)
    print dbObj['die_pause']
    print dbObj['dienstnehmer']['din_name']
    print dbObj['arbeitsplatz']['arp_bezeichnung']
    
    dbObj = Dienstnehmer()
    for i in range(1000):
        dbObj.get(45)
        name = dbObj['beschaeftigungsbereich']['beb_bezeichnung']
        
    """
    
    
    
    
    
import lib.Dienst 
import lib.Gehalt

