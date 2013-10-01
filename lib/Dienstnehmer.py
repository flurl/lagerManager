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
		
		
		
	def getRemainingSalary(self, date=None, excludeDutyId=None):
		remainingSalary = self['din_gehalt']
		print 'BP1 remainingSalary:', remainingSalary
		for d in self.getDuties(date, excludeDutyId):
			print 'BP2 remainingSalary:', remainingSalary
			remainingSalary -= d.getEarnings()
			
		print "BP3 remainingSalary for %s is %s" % (self['din_name'], remainingSalary)
		return remainingSalary
	
	
	"""def getRemainingHours(self, date=None):
		wr = self.findEmployeeWidgetRefByEmpId(dinId)
		beginDateTime = wr['beginDateTimeEdit'].dateTime()
		endDateTime = wr['endDateTimeEdit'].dateTime()
		
		remainingSalary = self.getRemainingSalary(date)
		remainingHours = (remainingSalary - globalConf['considerNAZ']*NACHTARBEITSZUSCHLAG*self.considerNAZForShift(beginDateTime, endDateTime) - TRINKGELDPAUSCHALE*tipAllowance)/hourlyRate
		
		return remainingHours"""
	
	def getDuties(self, date=None, excludeDutyId=None):
		monthBegin, monthEnd = datetimehelper.getMonthBeginEnd(date)
		
		query = """select die_id
				from dienste
				where 1=1
				and die_dinid = ?
				and die_beginn between ? and ?"""
				
		if excludeDutyId is not None:
			query +=  " and die_verid != %s" % excludeDutyId
		
		values = [self['din_id'], QtCore.QDateTime(monthBegin), QtCore.QDateTime(monthEnd)]
		
		res = self.runQuery(query, values)
		
		duties = []
		while res.next():
			duties.append(lib.Dienst.Dienst(res.value(0).toInt()[0]))
			
		return duties
	
	
	def getHourlyWage(self, date=None):
		hourly = self['gehalt']['stundensatz']
		print 'getHourlyWage:', date, hourly
		return hourly
	
	
if __name__ == '__main__':
	import sys
	import DBConnection
	import lib.Dienst
	print sys.argv
	DBConnection.connect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	
	"""dbObj = Dienstnehmer()
	dbObj.get(45)
	print unicode(dbObj['din_name'])
	
	print (("*"*20)+'\n')*5
	
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
	print dbObj['arbeitsplatz']['arp_bezeichnung']"""
	
	dbObj = Dienstnehmer()
	for i in range(1000):
		dbObj.get(45)
		name = dbObj['beschaeftigungsbereich']['beb_bezeichnung']
	
	
	
	
	
import lib.Dienst 
import lib.Gehalt

