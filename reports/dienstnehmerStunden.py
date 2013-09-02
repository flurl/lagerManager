# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.dienstnehmerStundenReport_gui import Ui_DienstnehmerStunden
from textReport import TextReport

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
		self.setData(self.mkQuery())
		self.process()
		
		
	def setupSignals(self):
		super(DienstnehmerStundenReport, self).setupSignals()
		self.connect(self.ui.comboBox_reportType, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
		self.connect(self.ui.pushButton_refresh, QtCore.SIGNAL('clicked()'), self.updateData)
		
		
	def setupUi(self):
		super(DienstnehmerStundenReport, self).setupUi()
		
		model = QtSql.QSqlTableModel()
		model.setTable('dienstnehmer')
		model.select()
		
		self.ui.comboBox_employees.setModel(model)
		self.ui.comboBox_employees.setModelColumn(model.fieldIndex('din_name'))
		
		self.ui.comboBox_employees.insertSeparator(-1)
		self.ui.comboBox_employees.setCurrentIndex(-1)
		
		
	
		
	def mkQuery(self):
		"""return the query"""
		reportType = unicode(self.ui.comboBox_reportType.currentText())
		pStart, pEnd = self._getCurrentPeriodStartEnd()
		
		selectedEmpIdx = self.ui.comboBox_employees.currentIndex()
		empId = None
		if selectedEmpIdx > 0:
			empModel = self.ui.comboBox_employees.model()
			empId = empModel.data(empModel.index(selectedEmpIdx, 0)).toInt()[0]
		
		
		query = """
				select {fields}
				from dienstnehmer, dienste, veranstaltungen, beschaeftigungsbereiche
				where 1=1
				and die_dinid = din_id
				and die_verid = ver_id
				and din_bebid = beb_id
				{empIdWhere}
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
							empIdWhere=("" if empId is None else " and din_id = %s "%(empId, ))
							)
			
		return query
	
