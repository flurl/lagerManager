# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from lib.LMDatabaseObject import LMDatabaseObject

class Gehalt(LMDatabaseObject):
	
	_DBTable = 'gehaelter'
	_dynamicColumns = {'stundensatz':'getHourlyWage'}
	
	
	def getHourlyWage(self, date=None):
		hourly = lib.Lohn.Lohn().findActive(self['geh_id'], date).next()['stundensatz']
		return hourly
	
	
	
import lib.Lohn