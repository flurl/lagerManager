# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.dienstnehmerStundenReport_gui import Ui_DienstnehmerStunden
from textReport import TextReport

import lib.Dienst

from lib.GlobalConfig import globalConf
from CONSTANTS import *



class DienstnehmerStundenReport(TextReport):
	
	uiClass = Ui_DienstnehmerStunden
	ident = 'dienstnehmerStunden'
	
	def __init__(self, parent=None):
		TextReport.__init__(self, parent)
				
		self.setHeader('Dienstnehmer Stunden Auswertung')
		self.setFooter('here could be a nice footer')
		self.defTableHeaders = [
								'DN Name',
								'DN Nummer',
								'Arbeitsstunden',
								'Pausestunden',
								'Anzahl der Dienste',
								'Lohn lt. Stunden',
								'Nachtarbeitszuschlag',
								'Trinkgeldpauschale',
								'Gesamt'
		]
		self.setTableHeaders(self.defTableHeaders)

		self.updateData()
		
		
	def updateData(self):
		data = []

		query =  self.mkQuery()
		results = self.db.exec_(query)
		while results.next():
			dieId = results.value(0).toInt()[0]
			d = lib.Dienst.Dienst(dieId)
			shift = d['schicht']
			emp = d['dienstnehmer']
			
			shiftName = shift['ver_bezeichnung']
			shiftDate = shift['ver_datum'].toPyDate()
			dutyBegin = d['die_beginn'].toPyDateTime()
			dutyEnd = d['die_ende'].toPyDateTime()
			empName = emp['din_name']
			empNr = emp['din_nummer']
			dutyHours = d.getTotalHours()
			workingHours = d.getWorkingHours()
			dutyPause = d['die_pause']
			count = 1
			shiftSalary = d.getEarnings()
			shiftNAZ = d.getNAZ()
			tipAllowance = emp['beschaeftigungsbereich']['beb_trinkgeldpauschale']*workingHours*globalConf['trinkgeldpauschale']
			shiftSum = shiftSalary
			shiftSalary = shiftSalary - shiftNAZ - tipAllowance
		
			l = [shiftDate, shiftName, empName, empNr, dutyBegin, dutyEnd, dutyHours, workingHours, dutyPause, count, shiftSalary, shiftNAZ, tipAllowance, shiftSum]
		
			data.append(l)
		
		self.dataFromDb = data
		
		self.setData(data)
		self.process()
		
	def setData(self, data):
		
		if data is None:
			data = self.dataFromDb
		
		
		reportType = unicode(self.ui.comboBox_reportType.currentText())
		
		dateFilter = self.ui.comboBox_timespan.itemData(self.ui.comboBox_timespan.currentIndex()).toInt()[0]
		if dateFilter > 0:
			if reportType == u'Jährlich':
				data = [row for row in data if row[0].year == dateFilter]
			else:
				data = [row for row in data if row[0].month == dateFilter]
		
		if reportType == u'Monatlich':
			data = self.groupBy(data, 'monthly')
			self.setTableHeaders(['Monat', 'Name', 'DN-Nr.', 'Anwesenheitsst.', 'Arbeitsstunden', 'Pause', 'Anzahl', 'Gehalt', 'NAZ', 'Trinkgeldp.', 'gesamt'])
			
		elif reportType == u'Jährlich':
			data = self.groupBy(data, 'yearly')
			self.setTableHeaders(['Jahr', 'Name', 'DN-Nr.', 'Anwesenheitsst.', 'Arbeitsstunden', 'Pause', 'Anzahl', 'Gehalt', 'NAZ', 'Trinkgeldp.', 'gesamt'])
		
		else:
			self.setTableHeaders(['Datum', 'Schicht', 'Name', 'DN-Nr.', 'Dienst Beginn', 'Dienst Ende', 'Anwesenheitsst.', 'Arbeitsstunden', 'Pause', 'Anzahl', 'Gehalt', 'NAZ', 'Trinkgeldp.', 'gesamt'])
			
		data.sort(key=lambda x: (x[0], x[1]))
		
		super(DienstnehmerStundenReport, self).setData(data)
		
		return True
		
	
		
	def setupSignals(self):
		super(DienstnehmerStundenReport, self).setupSignals()
		self.connect(self.ui.comboBox_reportType, QtCore.SIGNAL('currentIndexChanged(int)'), lambda: self.setupTimespanCombo() and self.setData(None) and self.process())
		self.connect(self.ui.pushButton_refresh, QtCore.SIGNAL('clicked()'), self.updateData)
		self.connect(self.ui.comboBox_employees, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
		self.connect(self.ui.comboBox_fieldOfEmployment, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
		self.connect(self.ui.comboBox_timespan, QtCore.SIGNAL('currentIndexChanged(int)'),  lambda: self.setData(None) and self.process())
		
		
	def setupUi(self):
		super(DienstnehmerStundenReport, self).setupUi()
		
		model = QtSql.QSqlTableModel()
		model.setTable('dienstnehmer')
		model.select()
		
		self.ui.comboBox_employees.setModel(model)
		self.ui.comboBox_employees.setModelColumn(model.fieldIndex('din_name'))
		
		self.ui.comboBox_employees.insertSeparator(-1)
		self.ui.comboBox_employees.setCurrentIndex(-1)
		
		model = QtSql.QSqlTableModel()
		model.setTable('beschaeftigungsbereiche')
		model.select()
		
		self.ui.comboBox_fieldOfEmployment.setModel(model)
		self.ui.comboBox_fieldOfEmployment.setModelColumn(model.fieldIndex('beb_bezeichnung'))
		
		self.ui.comboBox_fieldOfEmployment.insertSeparator(-1)
		self.ui.comboBox_fieldOfEmployment.setCurrentIndex(-1)
		
		self.setupTimespanCombo()
		
		
	def setupTimespanCombo(self):
		combo = self.ui.comboBox_timespan
		combo.clear()
		
		reportType = unicode(self.ui.comboBox_reportType.currentText())
		
		if reportType == u'Jährlich':
			query = QtSql.QSqlQuery()
			query.prepare("select distinct YEAR(die_beginn) from dienste order by YEAR(die_beginn) DESC")
			query.exec_()
			while query.next():
				combo.addItem(query.value(0).toString(), query.value(0))
		
		else:
			for i in range(1,13):
				combo.addItem(unicode(i), i)
				
		combo.insertSeparator(-1)
		combo.setCurrentIndex(-1)
		
		return True
		
		
	def groupBy(self, data, groupBy='monthly'):
		
		newData = []
		emps = {}
		
		for row in data:
			if groupBy == 'monthly':
				group = (row[0].year, row[0].month)
			elif groupBy == 'yearly':
				group = (row[0].year, )
				
			if group not in emps:
				emps[group] = {}
				
			try:
				emp = emps[group][row[3]] #row[3] = DN-Nr., which should be unique
			except KeyError:
				emps[group][row[3]] = emp = {'name': row[2],
										'number': row[3],
										'totalHours': 0.0, 
										'workingHours': 0.0, 
										'pause': 0.0, 
										'count': 0.0, 
										'salary': 0.0,
										'NAZ': 0.0,
										'tipAllowance': 0.0,
										'sum': 0.0
										}
			
			emp['totalHours'] += row[6]
			emp['workingHours'] += row[7]
			emp['pause'] += row[8]
			emp['count'] += row[9]
			emp['salary'] += row[10]
			emp['NAZ'] += row[11]
			emp['tipAllowance'] += row[12]
			emp['sum'] += row[13]
			
		for group in emps:
			for emp in emps[group]:
				e = emps[group][emp]
				newData.append([u'-'.join([unicode(x) for x in group]), e['name'], e['number'], e['totalHours'], e['workingHours'], e['pause'], e['count'], e['salary'], e['NAZ'], e['tipAllowance'], e['sum']])
		
		return newData
	
		
	def mkQuery(self):
		"""return the query"""
		reportType = unicode(self.ui.comboBox_reportType.currentText())
		pStart, pEnd = self._getCurrentPeriodStartEnd()
		
		selectedEmpIdx = self.ui.comboBox_employees.currentIndex()
		empId = None
		if selectedEmpIdx > 0:
			empModel = self.ui.comboBox_employees.model()
			empId = empModel.data(empModel.index(selectedEmpIdx, 0)).toInt()[0]
			
		selectedFOEIdx = self.ui.comboBox_fieldOfEmployment.currentIndex()
		foeId = None
		if selectedFOEIdx > 0:
			foeModel = self.ui.comboBox_fieldOfEmployment.model()
			foeId = foeModel.data(foeModel.index(selectedFOEIdx, 0)).toInt()[0]
		
		
		query = """
				select {fields}
				from dienstnehmer, dienste, veranstaltungen, beschaeftigungsbereiche
				where 1=1
				and die_dinid = din_id
				and die_verid = ver_id
				and din_bebid = beb_id
				{empIdWhere}
				{foeIdWhere}
				and ver_datum between '{pStart}' and '{pEnd}
				order by ver_datum desc'
				"""
		
		fields = 'die_id'
				
		query = query.format(
							fields=fields,
							pStart=pStart.strftime('%Y-%m-%d %H:%M:%S'), 
							pEnd=pEnd.strftime('%Y-%m-%d %H:%M:%S'),
							empIdWhere=("" if empId is None else " and din_id = %s "%(empId, )),
							foeIdWhere=("" if foeId is None else " and beb_id = %s "%(foeId, ))
							)
		
		return query
	
