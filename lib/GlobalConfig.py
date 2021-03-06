# -*- coding: utf-8 -*-

from PyQt4 import QtSql


class GlobalConfig(object):

	def __getitem__(self, key):
		val = self.getValueS(key)
		if not val is None and not val.isEmpty():
			return val
		else:
			val = self.getValueI(key)
			if not val is None:
				return val
			else:
				val = self.getValueF(key)
				if not val is None:
					return val
				else:
					raise KeyError



	def getValueS(self, key, date=None):
		"""returns the config value for key as string
		
		@key	the key that should be looked up
		"""
		return self.getValueFromDb(key, 'S', date)

	def getValueI(self, key, date=None):
		"""returns the config value for key as integer
		
		@key	the key that should be looked up
		"""
		return self.getValueFromDb(key, 'I', date)


	def getValueF(self, key, date=None):
		"""returns the config value for key as float
		
		@key	the key that should be looked up
		"""
		return self.getValueFromDb(key, 'F', date)

	
	
	def setValueS(self, key, val):
		"""sets the config key to the specified value as string
		
		@key	the key, that should be set
		@val	the value the option should be set to
		"""
		self.insertOrUpdateValue(key, val, 'S')
		

	def setValueI(self, key, val):
		"""sets the config key to the specified value as integer
		
		@key	the key, that should be set
		@val	the value the option should be set to
		"""
		self.insertOrUpdateValue(key, val, 'I')
	
	def setValueF(self, key, val):
		"""sets the config key to the specified value as float
		
		@key	the key, that should be set
		@val	the value the option should be set to
		"""
		self.insertOrUpdateValue(key, val, 'F')
	
	
	
	def getValueFromDb(self, key, type_, date=None):
		"""looks up a key in the config table and returns the value according to type_
		
		@key	the key to lookup
		@type_	type of the return value
		@date   the date for which the config key should be valid
		"""
		t = type_.upper()
		
		if date is None:
			dateWhere = ' and cfg_validTill >= now() order by cfg_validTill asc'
		elif isinstance(date, basestring):
			dateWhere = ' and cfg_validTill >= "%s" order by cfg_validTill asc' % date
		else:
			# convert eg. a QDateTime instance to python datetime 
			try:
				date = date.toPyDateTime()
			except AttributeError:
				pass
			dateWhere = ' and cfg_validTill >= "%s" order by cfg_validTill asc' % date.isoformat(' ')

		query = QtSql.QSqlQuery()
		if key == 'dbVersion':
			# special case:
			# the dbVersion is queried in the updater script
			# this fails for the update, where the cfg_validTill column is added
			# and there can only be 1 dbVersion value anyways
			query.prepare("select cfg_valueI from config where cfg_key = ?")
		elif t == 'I':
			query.prepare('select cfg_valueI from config where cfg_key = ? %s limit 1' % dateWhere)
		elif t == 'F':
			query.prepare('select cfg_valueF from config where cfg_key = ? %s limit 1' % dateWhere)
		else:
			query.prepare('select cfg_valueS from config where cfg_key = ? %s limit 1' % dateWhere)
			
		query.addBindValue(key)
		query.exec_()
		
		if query.lastError().isValid():
			print 'Error while selecting value from config for key %s'%key, query.lastError().text()
			return False
		
		if not query.size() > 0:
			return None
		
		query.next()
		
		if t == 'I':
			if query.isNull(0):
				value = None
			else:
				value = query.value(0).toInt()[0]
		elif t == 'F':
			if query.isNull(0):
				value = None
			else:
				value = query.value(0).toFloat()[0]
		else:
			if query.isNull(0):
				value = None
			else:
				value = query.value(0).toString()
			
		return value
	
	
	def insertOrUpdateValue(self, key, value, type_):
		"""this method inserts or updates a config key, depending on if the key already exists
		
		@key	the key to lookup
		@value	the value to set the config value to
		@type_	type of the config value
		"""
		t = type_.upper()
		
		query = QtSql.QSqlQuery()
		query.prepare('select count(*) from config where cfg_key = ?')
		query.addBindValue(key)
		query.exec_()
		if query.lastError().isValid():
			print 'Error while selecting count(*) from config for key %s'%key, query.lastError().text()
			return False
		
		query.next()
		
		count = query.value(0).toInt()[0]
		query = QtSql.QSqlQuery()
		if count != 0:
			if t == 'I':
				query.prepare('update config set cfg_valueI = ? where cfg_key = ? and cfg_validTill >= now()')
			elif t == 'F':
				query.prepare('update config set cfg_valueF = ? where cfg_key = ? and cfg_validTill >= now()')
			else:
				query.prepare('update config set cfg_valueS = ? where cfg_key = ? and cfg_validTill >= now()')
		
		else:
			if t == 'I':
				query.prepare('insert into config (cfg_valueI, cfg_key) values (?, ?)')
			elif t == 'F':
				query.prepare('insert into config (cfg_valueF, cfg_key) values (?, ?)')
			else:
				query.prepare('insert into config (cfg_valueS, cfg_key) values (?, ?)')
				
		query.addBindValue(value)
		query.addBindValue(key)
		
		query.exec_()
		if query.lastError().isValid():
			print 'Error while inserting or updating config for key %s'%key, query.lastError().text()
			return False
		
		return True


globalConf = GlobalConfig()
