# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from lib.LMDatabaseObject import LMDatabaseObject

class Lohn(LMDatabaseObject):
	
	_DBTable = 'loehne'
	_dynamicColumns = {'stundensatz':'getHourlyWage'}
	
	def findActive(self, gehId, date=None):
		if date is None:
			date = QtCore.QDateTime.currentDateTime()
		
		query = "select min(loh_validTill) from loehne where loh_gehid = ? and loh_validTill >= ?"
		values = [gehId, date]
		
		res = self.runQuery(query, values)
		res.next()
		
		minValid = res.value(0).toDateTime()
		
		return self.find([('loh_validTill', minValid), ('loh_gehid', gehId)])
	
	def getHourlyWage(self):
		return self['loh_summe']/173.0
		
