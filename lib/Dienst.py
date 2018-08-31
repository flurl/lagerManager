# -*- coding: utf-8 -*-
from PyQt4 import QtCore

from lib.LMDatabaseObject import LMDatabaseObject
from lib.Beschaeftigungsbereich import Beschaeftigungsbereich
from lib.Feiertag import Feiertag
from lib.LMDatabaseRelation import LMDatabaseRelation

from lib.GlobalConfig import globalConf
from CONSTANTS import *

class Dienst(LMDatabaseObject):

    _DBTable = 'dienste'
    """import sys
    print "#"*40
    dn = lib.Dienstnehmer.Dienstnehmer()
    print dir(sys.modules['lib.Dienstnehmer'])
    print dir(sys.modules['lib.Beschaeftigungsbereich'])
    print "#"*40"""
    dienstnehmer = LMDatabaseRelation('die_dinid', 'lib.Dienstnehmer.Dienstnehmer')
    arbeitsplatz = LMDatabaseRelation('die_arpid', 'lib.Arbeitsplatz.Arbeitsplatz')
    schicht = LMDatabaseRelation('die_verid', 'lib.Schicht.Schicht')


    def getEarnings(self):
        emp = lib.Dienstnehmer.Dienstnehmer(self['die_dinid'])
        foe = Beschaeftigungsbereich(emp['din_bebid'])

        hours = self.getWorkingHours()
        feiertagsStunden = self.getFeiertagszuschlagStunden()
        hourlyWage = emp.getHourlyWage(self['die_beginn'])
        #print "feiertagszuschlag für %s stunden" % feiertagsStunden
        salary = hours*hourlyWage+feiertagsStunden*hourlyWage+self.getNAZ()+foe['beb_trinkgeldpauschale']*globalConf.getValueF('trinkgeldpauschale', self['die_beginn'])*hours

        return salary


    def getWorkingHours(self):
        return self.getTotalHours()-self.getPauseHours()

    def getTotalHours(self):
        return round(self['die_beginn'].secsTo(self['die_ende'])/3600.0, 2)

    def getNAZ(self):
        if not globalConf['considerNAZ']:
            return 0

        beginDateTime = self['die_beginn']
        endDateTime = self['die_ende']

        NAZBegin = QtCore.QDateTime(beginDateTime)
        NAZBegin.setTime(QtCore.QTime(22, 0))

        NAZEnd = QtCore.QDateTime(beginDateTime)
        NAZEnd.setTime(QtCore.QTime(6, 0))

        midnight = QtCore.QDateTime(beginDateTime)
        midnight.setTime(QtCore.QTime(0, 0))

        if beginDateTime.time() < QtCore.QTime(6, 0):
            NAZBegin = NAZBegin.addDays(-1)
        else:
            NAZEnd = NAZEnd.addDays(1)
            midnight = midnight.addDays(1)


        timeOutOfNAZ = 0		
        interval0 = beginDateTime.secsTo(NAZBegin)
        interval1 = endDateTime.secsTo(NAZEnd)

        if interval0 > 0:
            timeOutOfNAZ += interval0

        if interval1 < 0:
            timeOutOfNAZ += abs(interval1)

        timeWithinNAZ = beginDateTime.secsTo(endDateTime) - timeOutOfNAZ

        #print "checking NAZ: begin:",beginDateTime.toPyDateTime(), "end:", endDateTime.toPyDateTime(), "NAZBegin: ", NAZBegin.toPyDateTime(), "NAZEnd:", NAZEnd.toPyDateTime(), "shiftLen:", beginDateTime.secsTo(endDateTime)/3600.0, 'withinNAZ:', timeWithinNAZ/3600.0, 'outOfNAZ:', timeOutOfNAZ/3600.0 
        
        if timeWithinNAZ > timeOutOfNAZ:
            #print "Considering NAZ"
            return globalConf.getValueF('nachtarbeitszuschlag', self['die_beginn'])

        #print "Not considering NAZ"
        return 0
        
        
    def getFeiertagszuschlagStunden(self):
        #print "getFeiertagszuschlagStunden()"
        hours = 0.0
        beginDateTime = QtCore.QDateTime(self['die_beginn'])
        endDateTime = QtCore.QDateTime(self['die_ende'])
        beginDateTime.setTime(QtCore.QTime(0, 0))
        endDateTime.setTime(QtCore.QTime(0, 0))
        beginFeiertag = Feiertag().find([('fta_datum', beginDateTime)])
        if beginFeiertag.next():
            #print "Feiertag gefunden am %s" % self['die_beginn']
            #start and end on same day
            if beginDateTime.secsTo(endDateTime) == 0:
                return self.getWorkingHours()
            hours += round(self['die_beginn'].secsTo(beginDateTime.addDays(1))/3600.0, 2)
            
        endFeiertag = Feiertag().find([('fta_datum', endDateTime)])
        while endFeiertag.next():
            #print "Feiertag gefunden am %s" % self['die_ende']
            hours += round(endDateTime.secsTo(self['die_ende'])/3600.0, 2)
        
        return hours

    def getPauseHours(self):
        #pausen werden jetzt als arbeitszeit mitbezahlt -> keine pausenberechnung mehr nötig
        return 0.0

if __name__ == '__main__':
    import sys
    print sys.argv
    DBConnection.connect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    dbObj = Dienst()
    dbObj.get(768)
    print dbObj['die_pause']
    print dbObj['dienstnehmer']

    print (("*"*20)+'\n')*5





import lib.Dienstnehmer
