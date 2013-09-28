# -*- coding: utf-8 -*-
#from PyQt4 import QtSql, QtCore

#import DBConnection
import sys
import importlib


class LMDatabaseRelation(object):

	def __init__(self, first, second):
		self.__column = first
		self.__other = second
		self.__class = None
		self.__type = 'Nto1'


	def __loadModule(self):
		if self.__class is None:
			other = self.__other
			otherModule = other.rpartition('.')[0]
			otherClass = other.rpartition('.')[2]
			print 'importing', otherModule, otherClass
			try:
				print dir(sys.modules[otherModule])
			except:
				print 'EXCEXPTION'
			ret = __import__(otherModule)
			print dir(sys.modules[otherModule])
			someClass = getattr(sys.modules[otherModule], otherClass)
			self.__class = someClass
		
		
	def __call__(self):
		try:
			self.__loadModule()
		except ValueError:
			tmp = self.__column
			self.__column = self.__other
			self.__other = tmp
			self.__type = '1toN'
			self.__loadModule()
		
		if self.__type == 'Nto1':
			obj = self.__class(self.__pkObject[self.__column])
		elif self.__type == '1toN':
			obj = self.__class()
			obj.find(self.__column, self.__pkObject[self.__pkObject.primaryKey])
		
		return obj
	
	def register(self, obj):
		self.__pkObject = obj