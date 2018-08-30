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
		self._filterCondition = None
		self.isDirty = False
		self.isNew = True
		
		self.__model = QtSql.QSqlTableModel()
		self.__model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
		self.__model.setTable(self._DBTable)
		self.__pointer = 0
		self.__len = None
		
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
			c['value'] = QtCore.QDate(value)
			
		else:
			raise Exception('unknown column type %s' % c['type'])
		
		self.isDirty = True
		
		
	def __iter__(self):
		while self.__loadNextRecord():
			yield self 
			
			
	def __len__(self):
		if self.__len is not None:
			return self.__len
		
		if self._filterCondition is None:
			self.__len = self.__model.rowCount()
		else:
			self.__len = 0
			pointer = self.__pointer
			self.__pointer = 0
			while self.next():
				self.__len += 1
			self.__pointer = pointer
			
		return self.__len
			
		
		
			
		
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
				
				self._columns[unicode(field.name())] = {'type': field.type(), 'required': field.requiredStatus()}
			
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
		
		if self._filterCondition is not None:
			if not self[self._filterCondition[0]] == self._filterCondition[1]:
				return self.__loadNextRecord()
		
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
	
		
	
	
	def find(self, first=None, second=None, orderBy=None):
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
		
		if orderBy is not None:
			self.__model.setSort(self.__model.fieldIndex(orderBy[0]), QtCore.Qt.AscendingOrder if orderBy[1].upper() == 'ASC' else QtCore.Qt.DescendingOrder)
		
		self.__model.select()
		self.isNew = False
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
		
		self.find(self.primaryKey, pk)
		
		self.__readCache[self._DBTable]['queries']['get'][pk] = query
		self.isNew = False
			
		
	def filter(self, column, value):
		self._filterCondition = (column, value)
		
	
	def validate(self):
		for name in self._columns:
			col = self._columns[name]
			type_ = col['type']
			req = col['required']
			if req and not (name == self.primaryKey and self.isNew):
				if self[name] == '' or self[name] is None:
					raise ValueError("%s is required" % name)
					
		return True
				
			
	
	
	def save(self):
		if self.isDirty:
			m = self.__model
			if self.isNew:
				record = m.record(self.__pointer)
			else:
				record = m.record(self.__pointer)
				
			for col in self._columns:
				if self.isNew and col == self.primaryKey:
					continue
				try:
					record.setValue(col, QtCore.QVariant(self[col]))
				except KeyError:
					record.setValue(col, QtCore.QVariant())
				
			if self.isNew:
				m.insertRecord(-1, record)
			else:
				m.setRecord(self.__pointer, record)
			
			m.submitAll()
			self.isDirty = False
			self.isNew = False
		
	def clearQueryCache(self):
		for table in self.__readCache:
			self.__readCache[table]['queries']['get'] = {}
		
