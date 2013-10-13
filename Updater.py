# -*- coding: utf-8 -*-
import glob
import re

from DBConnection import dbConn

from lib.GlobalConfig import globalConf
import version

class UnversionedSQLFileError(Exception):
	pass

class ScriptSQLError(Exception):
	pass


class Updater(object):
	
	def checkForDatabaseUpdates(self):
		currVersion = globalConf.getValueI('dbVersion')
		
		if currVersion < version.VERSION:
			updates = self.getAvailableUpdates()
			if len(updates):
				return True
		
		return False
		
	
	def getAvailableUpdates(self):
		updFiles = glob.glob('sql/upd*.sql')
		updFiles.sort(reverse=True)
		return updFiles
	
	
	def installDatabaseUpdates(self):
		currVersion = globalConf.getValueI('dbVersion')
		files = self.getAvailableUpdates()
		pattern = re.compile(r'(#V)(\d*)$') #e.g. #V0001
		
		for f in files:
			with open('%s'%f, 'r') as content_file:
				lines = content_file.readlines()
			
			match = pattern.match(lines[0])
			if not match:
				raise UnversionedSQLFileError('No version found in %s'%f)
			
			groups = match.groups()
			if not groups:
				raise UnversionedSQLFileError('Versionstring "%s" invalid in file %s'%(lines[0], f))
			
			fileVersion = int(groups[1])
			
			
			if fileVersion <= currVersion:
				break
			
			self.runScript(lines)
		
		globalConf.setValueI('dbVersion', version.VERSION)
		
		return True
		
			
	def runScript(self, lines):
		query = '\n'.join(lines)
		print "runScript:", query
		query = dbConn.exec_(query)
		if query.lastError().isValid():
			raise ScriptSQLError('Error while running script:\n' + '\n'.join(lines) + query.lastError().text())
		
		