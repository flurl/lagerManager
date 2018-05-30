# -*- coding: utf-8 -*-
from PyQt4 import QtSql, QtCore

import DBConnection
from lib.LMDatabaseRelation import LMDatabaseRelation

import collections
import copy

class DatabaseError(Exception):
	pass
	


class LMDatabaseObject(object):

	__readCache = {}

	def __init__(self, pk=None):
		self.primaryKey = None
		
		self._columns = {}
		self._relations = {}
		
		self.__model = QtSql.QSqlTableModel()
		self.__model.setTable(self._DBTable)
		self.__pointer = 0
		
		if not self._DBTable in self.__readCache.keys():
			self.__readCache[self._DBTable] = {'columns':{}, 'queries': {'get':{}}}
		
		self.__loadTableColumns()
		self.__setupRelations()
		if pk is not None:
			self.get(pk)
		
		
	
	def __getitem__(self, name):
		#try:
		
		if hasattr(self, '_dynamicColumns'):
			if name in self._dynamicColumns.keys():
				return getattr(self, self._dynamicColumns[name])()
		
		if name in self._relations.keys():
			return self._relations[name]()
			
		return self._columns[name]['value']
		#except:
		#	raise KeyError
	
	
	def __setitem__(self, name, value):
		c = self._columns[name]
	
		if c['type'] == QtCore.QVariant.Double:
			c['value'] = value
			
		elif c['type'] in [QtCore.QVariant.UInt, QtCore.QVariant.Int]:
			c['value'] = value
			
		elif c['type'] == QtCore.QVariant.String:
			c['value'] = QtCore.QString(value)
			
		elif c['type'] == QtCore.QVariant.DateTime:
			c['value'] = QtCore.QDateTime(value)
		
		elif c['type'] == QtCore.QVariant.Time:
			c['value'] = QtCore.QTime(value)
			
		elif c['type'] == QtCore.QVariant.Date:
			value = QtCore.QDate(value)
			
		else:
			raise Exception('unknown column type %s' % c['type'])
		
		
	def __iter__(self):
		while self.__loadNextRecord():
			yield self 
				
			
		
	def __loadTableColumns(self):
		if 'definitions' in self.__readCache[self._DBTable]['columns']:
			self._columns = copy.deepcopy(self.__readCache[self._DBTable]['columns']['definitions'])
			self.primaryKey = copy.deepcopy(self.__readCache[self._DBTable]['columns']['primaryKey'])
		else:
			self._columns = {}
			table = self._DBTable
			
			driver = DBConnection.dbConn.driver()
			rec = driver.record(table)
			
			for i in range(rec.count()):
				field = rec.field(i)
				"""print field.name()
				print field.type()
				print field.precision()
				print field.isGenerated()
				print field.isAutoValue()"""
				
				#assumme this is the primary key 
				if field.isAutoValue():
					#print 'using %s as primary key' % field.name()
					self.primaryKey = unicode(field.name())
				
				self._columns[unicode(field.name())] = {'type': field.type()}
			
			self.__readCache[self._DBTable]['columns']['definitions'] = self._columns
			self.__readCache[self._DBTable]['columns']['primaryKey'] = self.primaryKey
		
		
	def __setupRelations(self):
		d = self.__class__.__dict__
		for var in d:
			if isinstance(d[var], LMDatabaseRelation):
				d[var].register(self)
				self._relations[var] = d[var]
		
	
	
		
	def __storeValueFromDb(self, value, col):
		type_ = self._columns[col]['type']
		
		if type_ == QtCore.QVariant.Double:
			value = value.toFloat()[0]
			
		elif type_ in [QtCore.QVariant.UInt, QtCore.QVariant.Int]:
			value = value.toInt()[0]
			
		elif type_ == QtCore.QVariant.String:
			value = value.toString()
			
		elif type_ == QtCore.QVariant.DateTime:
			value = value.toDateTime()
			
		elif type_ == QtCore.QVariant.Time:
			value = value.toTime()
			
		elif type_ == QtCore.QVariant.Date:
			value = value.toDate()
			
		else:
			raise Exception('unknown column type %s' % type_)
		
		self._columns[col]['value'] = value
		
		
	def __loadNextRecord(self):
		m = self.__model
		#TODO: only select if not already done
		m.select()
		count = m.rowCount()
		
		if self.__pointer >= count:
			self.__pointer = 0
			return False
		
		
		record = m.record(self.__pointer)
		for col in self._columns:
			value = record.value(col)
			self.__storeValueFromDb(value, col)
		
		self.__pointer += 1
		
		return self
			
			
	def next(self):
		return self.__loadNextRecord()
			
		

	
	def runQuery(self, query, values=[]):

		q = QtSql.QSqlQuery()
		q.prepare(query)
		
		for v in values:
			q.addBindValue(v)
			
		q.exec_()
		
		if q.lastError().isValid():
			print "Query raised an error:\n", q.lastError().text(), '\n', query, '\n', values
			raise DatabaseError
		
		return q
	
		
	
	
	def find(self, first=None, second=None):
		filterStr = u''
		if isinstance(first, basestring):
			if self._columns[first]['type'] in [QtCore.QVariant.String, QtCore.QVariant.DateTime]:
				second = u"'%s'"%second
			filterStr = "%s = %s"%(first, second)
		
		elif isinstance(first, collections.Iterable):
			for obj in first:
				col = obj[0]
				val = obj[1]
				
				try:
					operator = obj[2]
				except IndexError:
					operator = '='
				
				if self._columns[col]['type'] in [QtCore.QVariant.String, QtCore.QVariant.DateTime]:
					if isinstance(val, QtCore.QDateTime):
						val = val.toPyDateTime()
					elif isinstance(val, QtCore.QDate):
						val = val.toPyDate()
					elif isinstance(val, QtCore.QTime):
						val = val.toPyTime()
					val = u"'%s'"%val
					
				filterStr += 'and %s %s %s ' % (col, operator, val)
				
		#remove the first 'and' if it exists
		before, sep, after = filterStr.partition(u'and')
		if before == u'':
			filterStr = after
		
		self.__model.setFilter(filterStr)
		self.__model.select()
		return self
		
	
	
		
	def get(self, pk):
		if pk in self.__readCache[self._DBTable]['queries']['get'].keys():
			query = self.__readCache[self._DBTable]['queries']['get'][pk]
		else:
			query = "select %s from %s where %s = %s" % (','.join(self._columns.keys()), self._DBTable, self.primaryKey, pk)
			query = self.runQuery(query)
			
		query.first()
		
		for col in self._columns:
			value = query.value(query.record().indexOf(col))
			self.__storeValueFromDb(value, col)
			
		self.__readCache[self._DBTable]['queries']['get'][pk] = query
			
		
	
