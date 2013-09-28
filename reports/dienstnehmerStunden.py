# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.dienstnehmerStundenReport_gui import Ui_DienstnehmerStunden
from textReport import TextReport

import lib.Dienst

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
			tipAllowance = emp['beschaeftigungsbereich']['beb_trinkgeldpauschale']*workingHours
			shiftSum = shiftSalary+tipAllowance
		
			l = [shiftDate, shiftName, empName, empNr, dutyBegin, dutyEnd, dutyHours, workingHours, dutyPause, count, shiftSalary, shiftNAZ, tipAllowance, shiftSum]
		
			data.append(l)
		
		self.dataFromDb = data
		
		self.setData(data)
		self.process()
		
	def setData(self, data):
		
		if data is None:
			data = self.dataFromDb
		
		
		reportType = unicode(self.ui.comboBox_reportType.currentText())
		
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
		self.connect(self.ui.comboBox_reportType, QtCore.SIGNAL('currentIndexChanged(int)'), lambda: self.setData(None) and self.process())
		self.connect(self.ui.pushButton_refresh, QtCore.SIGNAL('clicked()'), self.updateData)
		self.connect(self.ui.comboBox_employees, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
		self.connect(self.ui.comboBox_fieldOfEmployment, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
		
		
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
		
		
	def groupBy(self, data, groupBy='monthly'):
		
		newData = []
		currTimespan = None
		emps = {}
		
		for row in data:
			if groupBy == 'monthly':
				timespan = (row[0].year, row[0].month)
			elif groupBy == 'yearly':
				timespan = (row[0].year)
				
			if timespan != currTimespan:
				currTimespan = timespan
				emps[currTimespan] = {}
				
			try:
				emp = emps[timespan][row[3]] #row[3] = DN-Nr., which should be unique
			except KeyError:
				emps[timespan][row[3]] = emp = {'name': row[2],
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
			
		for timespan in emps:
			for emp in emps[timespan]:
				e = emps[timespan][emp]
				newData.append([timespan, e['name'], e['number'], e['totalHours'], e['workingHours'], e['pause'], e['count'], e['salary'], e['NAZ'], e['tipAllowance'], e['sum']])
		
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
				
				
		
		query = """
				select {fields}
				from dienstnehmer, dienste, veranstaltungen, beschaeftigungsbereiche
				where 1=1
				and die_dinid = din_id
				and die_verid = ver_id
				and din_bebid = beb_id
				{empIdWhere}
				{foeIdWhere}
				and ver_datum between '{pStart}' and '{pEnd}'
				group by {groupByFields}
				"""
				
		nachtarbeitszuschlagQuery = """
			sum(if (
				if(die_beginn < concat(date(die_beginn), ' 06:00:00'), 
					if (concat(date(die_beginn), ' 06:00:00') >= die_ende, 
					time_to_sec(timediff(die_ende, die_beginn)),
					time_to_sec(timediff(concat(date(die_beginn), ' 06:00:00'), die_beginn))), 
					if(die_beginn >= concat(date(die_beginn), ' 22:00:00'),
					if (adddate(concat(date(die_beginn), ' 06:00:00'), INTERVAL 1 DAY) > die_ende, 
						time_to_sec(timediff(die_ende, die_beginn)), 
						time_to_sec(timediff(adddate(concat(date(die_beginn), ' 06:00:00'), INTERVAL 1 DAY), die_beginn))
					),
					if (adddate(concat(date(die_beginn), ' 06:00:00'), INTERVAL 1 DAY) > die_ende, 
						time_to_sec(timediff(die_ende, concat(date(die_beginn), ' 22:00:00'))), 
						time_to_sec(timediff(adddate(concat(date(die_beginn), ' 06:00:00'), INTERVAL 1 DAY), concat(date(die_beginn), ' 22:00:00')))
					)
					)
				) > time_to_sec(timediff(die_ende, die_beginn))/2,
				1,
				0
				)*%s)
		"""%(NACHTARBEITSZUSCHLAG, )
			 
				
		if reportType == u'Jährlich':
			fields = 'din_name, din_nummer, sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause), sum(die_pause), count(*), (sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause))*din_stundensatz, ' + nachtarbeitszuschlagQuery + ', {TRINKGELDPAUSCHALE}*(sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause))*beb_trinkgeldpauschale, ' + nachtarbeitszuschlagQuery + ' + (sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause))*din_stundensatz + {TRINKGELDPAUSCHALE}*(sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause))*beb_trinkgeldpauschale '
			groupByFields = 'din_id, din_name, din_nummer'
			
			self.setTableHeaders(self.defTableHeaders)
			
		elif reportType == u'Monatlich':
			fields = 'monthname(ver_datum), din_name, din_nummer, sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause), sum(die_pause), count(*), (sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause))*din_stundensatz, ' + nachtarbeitszuschlagQuery + ', {TRINKGELDPAUSCHALE}*(sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause))*beb_trinkgeldpauschale, ' + nachtarbeitszuschlagQuery + ' + (sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause))*din_stundensatz + {TRINKGELDPAUSCHALE}*(sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause))*beb_trinkgeldpauschale '
			groupByFields = 'monthname(ver_datum), din_id, din_name, din_nummer'
			
			self.setTableHeaders(['Monat']+self.defTableHeaders)
			
		else:
			fields = 'ver_bezeichnung, ver_datum, din_name, din_nummer, sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause), sum(die_pause), count(*), (sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause))*din_stundensatz, ' + nachtarbeitszuschlagQuery + ', {TRINKGELDPAUSCHALE}*(sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause))*beb_trinkgeldpauschale, ' + nachtarbeitszuschlagQuery + ' + (sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause))*din_stundensatz + {TRINKGELDPAUSCHALE}*(sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600) - sum(die_pause))*beb_trinkgeldpauschale '
			groupByFields = 'ver_id, ver_bezeichnung, ver_datum, din_id, din_name, din_nummer'
			
			self.setTableHeaders(['Schicht', 'Datum']+self.defTableHeaders)
			
		fields = fields.format(TRINKGELDPAUSCHALE=TRINKGELDPAUSCHALE)
			
		query = query.format(
							fields=fields,
							groupByFields=groupByFields,
							pStart=pStart.strftime('%Y-%m-%d %H:%M:%S'), 
							pEnd=pEnd.strftime('%Y-%m-%d %H:%M:%S'),
							empIdWhere=("" if empId is None else " and din_id = %s "%(empId, )),
							foeIdWhere=("" if foeId is None else " and beb_id = %s "%(foeId, ))
							)
			
		return query
	
