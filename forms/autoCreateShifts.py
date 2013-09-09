# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection
import config
from lib.GlobalConfig import globalConf

from forms.formBase import FormBase
from ui.forms.autoCreateShiftsForm_gui import Ui_AutoCreateShiftsForm

import datetime

class AutoCreateShiftsForm(FormBase):
	
	uiClass = Ui_AutoCreateShiftsForm
	ident = 'autoCreateShifts'
	
	def setupUi(self):
		super(AutoCreateShiftsForm, self).setupUi()
		self.ui.dateTimeEdit_shift.setDate(QtCore.QDate.currentDate())
		
		try:
			lastImportURL = config.config['connection'][DBConnection.connName]['last_shift_import_url']
		except KeyError:
			lastImportURL = ''
			
		self.ui.lineEdit_URL.setText(lastImportURL)
		
		
		try:
			lastImportedShiftDateTime = globalConf['last_imported_shift_datetime']
		except KeyError:
			lastImportedShiftDateTime = QtCore.QDateTime.currentDateTime().toTime_t()
			
		dt = QtCore.QDateTime()
		dt.setTime_t(lastImportedShiftDateTime)
		
		self.ui.dateTimeEdit_ignoreBefore.setDateTime(dt)
		
	
	def setupSignals(self):
		super(AutoCreateShiftsForm, self).setupSignals()
		self.connect(self.ui.pushButton_createShifts, QtCore.SIGNAL('clicked()'), self.createShifts)
		
		
		
	def createShifts(self):
		idx = self.ui.tabWidget.currentIndex()
		
		if idx == 0:
			self.createRecurringShifts()
		elif idx == 1:
			self.importShifts()
			
			
	def createRecurringShifts(self):
		recurrence = self.ui.comboBox_recurrence.currentIndex()
		count = self.ui.spinBox_recurrenceCount.value()
		name = self.ui.lineEdit_shiftName.text()
		beginDate = self.ui.dateTimeEdit_shift.date()
		beginTime = self.ui.dateTimeEdit_shift.time()
		
		self.beginTransaction()
		
		for i in range(count):
			date = beginDate
			if recurrence == 0:
				date = date.addDays(i*1)
			elif recurrence == 1:
				date = date.addDays(i*7)
			elif recurrence == 2:
				date = date.addMonths(i*1)
			elif recurrence == 3:
				date = date.addYears(i*1)
			
			if not self.createShift(name, date, beginTime):
				self.rollback()
				QtGui.QMessageBox.critical(self, u'Schichterstellung fehlgeschlagen', 
											u'Die Schichten konnten nicht erstellt werden!\nBitte kontaktieren Sie Ihren Datenbank Administrator')
			
		self.commit()
		QtGui.QMessageBox.information(self, u'Schichterstellung erfolgreich', 
										u'Die Schichten wurden erfolgreich erstellt')
		return True
			
			
			
	def importShifts(self):
		from lib.feedparser import feedparser
		
		url = unicode(self.ui.lineEdit_URL.text())

		feed = feedparser.parse(url)

		self.beginTransaction()
		maxDateTime = ignoreBefore = self.ui.dateTimeEdit_ignoreBefore.dateTime()
		for item in feed['items']:
			name = item['title']
			dateTime = item['published'][:-6] #strip the last 6 chars for easier parsing below
			dateTime = QtCore.QDateTime.fromString(dateTime, 'ddd, dd MMM yyyy hh:mm:ss')
			
			if dateTime <= ignoreBefore:
				continue
			
			beginDate = dateTime.date()
			beginTime = dateTime.time()
			
			if dateTime > maxDateTime:
				maxDateTime = dateTime
		
			if not self.createShift(name, beginDate, beginTime):
				self.rollback()
				QtGui.QMessageBox.critical(self, u'Schichterstellung fehlgeschlagen', 
											u'Die Schichten konnten nicht erstellt werden!\nBitte kontaktieren Sie Ihren Datenbank Administrator')
				
		self.commit()
		QtGui.QMessageBox.information(self, u'Schichterstellung erfolgreich', 
										u'Die Schichten wurden erfolgreich import')
		
		config.config['connection'][DBConnection.connName]['last_shift_import_url'] = url
		config.config.write()
		
		globalConf.setValueI('last_imported_shift_datetime', maxDateTime.toTime_t())
		
		return True


	def createShift(self, name, date, beginTime):
		query = QtSql.QSqlQuery()
			
		query.prepare('insert into veranstaltungen (ver_datum, ver_bezeichnung, ver_beginn) values (?, ?, ?)')
		query.addBindValue(date)
		query.addBindValue(name)
		query.addBindValue(beginTime)
		
		query.exec_()
		if query.lastError().isValid():
			print "Error while creating shift!", query.lastError().text()
			return False
		
		return True
	
	