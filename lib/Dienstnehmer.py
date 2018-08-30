# -*- coding: utf-8 -*-
from PyQt4 import QtCore

from lib import datetimehelper

from lib.LMDatabaseObject import LMDatabaseObject
from lib.LMDatabaseRelation import LMDatabaseRelation

from lib.DienstnehmerEreignisTyp import DienstnehmerEreignisTyp


class Dienstnehmer(LMDatabaseObject):
    
    _DBTable = 'dienstnehmer'
    _dynamicColumns = {'din_stundensatz': 'getHourlyWage', 'din_name': 'getName'}
    dienste = LMDatabaseRelation('lib.Dienst.Dienst', 'die_dinid')
    gehalt = LMDatabaseRelation('din_gehid', 'lib.Gehalt.Gehalt')
    beschaeftigungsbereich = LMDatabaseRelation('din_bebid', 'lib.Beschaeftigungsbereich.Beschaeftigungsbereich')
    ereignisse = LMDatabaseRelation('lib.DienstnehmerEreignis.DienstnehmerEreignis', 'dir_dinid')
    
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
        
    def getName(self):
        return self['din_nachname'] + u' ' + self['din_vorname']
    
    
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
        
        #countAvg = countTotal/numberOfDatapoints
        #hoursAvg = hoursTotal/numberOfDatapoints
        #nazAvg = nazTotal/numberOfDatapoints
        countAvg = countTotal/period
        hoursAvg = hoursTotal/period
        nazAvg = nazTotal/period
        
        print "countAvg:", countAvg, "hoursAvg:", hoursAvg
        return (numberOfDatapoints, countAvg, hoursAvg, nazAvg)
        
        
    def getVacationDays(self):
        eintritt = self.getLastEintritt()
        daysSinceEintritt = datetimehelper.daysBetween(eintritt['dir_datum'].toPyDateTime(), datetimehelper.now())
        weeksSinceEintritt = daysSinceEintritt // 7
        period = min(104, weeksSinceEintritt)
        avg = self.getAvg('weekly', period)
        vacationDays = (period/52)*avg[1]*5
        print "vacationDays:", vacationDays, "daysPerWeek", avg[1]
        return vacationDays
        
        
    def getOpenVacationDays(self):
        totalDays = self.getVacationDays()
        usedDays = self.getUsedVacationDays()
        openDays = totalDays - usedDays
        print "openDays:", openDays
        return openDays
        
        
    def getUsedVacationDays(self):
        #query = "select dir_id from dienstnehmer_ereignisse, dir_typen where dir_dinid = %s and dir_ditid = dit_id and dit_kbez in ('URBEG', 'UREND') order by dir_datum desc" % (self['din_id'], )
        #results = self.db.exec_(query)
        #ereignisse = []
        #while results.next():
        #    ereignisse.append(lib.DienstnehmerEreignis.DienstnehmerEreignis(results.values(0).toInt()[0]))
        #print ereignisse
        beginnDitId = lib.DienstnehmerEreignisTyp.DienstnehmerEreignisTyp().find('dit_kbez', 'URBEG').next()['dit_id']
        endeDitId = lib.DienstnehmerEreignisTyp.DienstnehmerEreignisTyp().find('dit_kbez', 'UREND').next()['dit_id']
        
        print beginnDitId, endeDitId
        ereignisse = self['ereignisse']
        ereignisse.filter('dir_ditid', beginnDitId)
        ub = []
        for e in ereignisse:
            ub.append(e['dir_datum'].toPyDateTime())
        ub.sort()
        
        ereignisse.filter('dir_ditid', endeDitId)
        ue = []
        for e in ereignisse:
            ue.append(e['dir_datum'].toPyDateTime())
        ue.sort()
        
        eintritt = self.getLastEintritt()
        daysSinceEintritt = datetimehelper.daysBetween(eintritt['dir_datum'].toPyDateTime(), datetimehelper.now())
        weeksSinceEintritt = daysSinceEintritt // 7
        period = min(104, weeksSinceEintritt)
        avg = self.getAvg('weekly', period)
        
        print ub
        print ue
        print avg
        periodBeginn = datetimehelper.addWeeks(datetimehelper.now(), period*-1)
        usedDays = 0.0
        for i in range(len(ub)):
            if ub[i] >= periodBeginn or ue[i] >= periodBeginn:
                usedDays += datetimehelper.daysBetween(ue[i], ub[i])*(avg[1]/7)
                
        print "usedDays:", usedDays
        return usedDays
                
       
    def getLastEintritt(self):
        eintrittDitId = lib.DienstnehmerEreignisTyp.DienstnehmerEreignisTyp().find('dit_kbez', 'EIN').next()['dit_id']
        eintritt = lib.DienstnehmerEreignis.DienstnehmerEreignis().find('dir_dinid', self['din_id'], orderBy=('dir_datum', 'desc'))
        eintritt.filter('dir_ditid', eintrittDitId)
        return eintritt.next()
        
        
    def getEreignisse(self, kbez=None, sorting='asc'):
        ereignisse = lib.DienstnehmerEreignis.DienstnehmerEreignis().find('dir_dinid', self['din_id'], ('dir_datum', sorting))
        if kubez is not None:
            typ = lib.DienstnehmerEreignisTyp.DienstnehmerEreignisTyp().find('dit_kbez', kbez)
            ereignisse.filter('dir_ditid', typ['dit_id'])
        return ereignisse
        
        
    def validateEreignisse(self):
        benoetigteTypen = DienstnehmerEreignisTyp().find('dit_benoetigt', 1)
        dnEreignisse = self['ereignisse']
        for bt in benoetigteTypen:
            found = False
            for de in dnEreignisse:
                if de['dir_ditid'] == bt['dit_id']:
                    found = True
            if found == False:
                raise LookupError("Ereignis %s ist erforderlich" % bt)
        return True
        
        
    def __unicode__(self):
        return unicode(self['din_nummer']) + u' - ' + unicode(self['din_name'])
        
    def __str__(self):
        return unicode(self).encode('utf-8')
    
    
if __name__ == '__main__':
    import sys
    import DBConnection
    import lib.Dienst
    print sys.argv
    DBConnection.connect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    
    dn = Dienstnehmer(72)
    print dn
    
    dbObj = Dienstnehmer()
    dbObj.get(30)
    print unicode(dbObj['din_name'])
    
    print (("*"*20)+'\n')*5
    dbObj['din_vorname'] = u"Pupsi"
    dbObj.save()
    
    #dbObj.getUsedVacationDays()
    dbObj.getOpenVacationDays()
    
    #ereignisse = dbObj['ereignisse']
    #ereignisse.filter('dir_ditid', 2)
    #while ereignisse.next():
    #    print ereignisse
    
    #dn = Dienstnehmer().find()
    #dns = []
    #while dn.next():
    #    dns.append((unicode(dn), dn.getAvg('monthly', 12)))
    #for d in dns:
    #    print d
    
    #while dbObj.next():
    #    print unicode(dbObj['din_name'])
    
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
import lib.DienstnehmerEreignis
import lib.DienstnehmerEreignisTyp

