# -*- coding: utf-8 -*-
from PyQt4 import QtCore

from lib.LMDatabaseObject import LMDatabaseObject

class Schicht(LMDatabaseObject):
	
	_DBTable = 'veranstaltungen'
	_dynamicColumns = {'date_time': 'getDateTime'}
	
	
	def getDateTime(self):
		dt = QtCore.QDateTime()
		dt.setDate(self['ver_datum'])
		dt.setTime(self['ver_beginn'])
		return dt
	
		
		