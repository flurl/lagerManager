# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.dienstnehmerStundenReport_gui import Ui_DienstnehmerStunden
from textReport import TextReport



class DienstnehmerStundenReport(TextReport):
	
	uiClass = Ui_DienstnehmerStunden
	ident = 'dienstnehmerStunden'
	
	def __init__(self, parent=None):
		TextReport.__init__(self, parent)
				
		self.setHeader('Dienstnehmer Stunden Auswertung')
		self.setFooter('here could be a nice footer')

		self.updateData()
		
	def updateData(self):
		self.setData(self.mkQuery())
		self.process()
		
		
	def setupSignals(self):
		super(DienstnehmerStundenReport, self).setupSignals()
		self.connect(self.ui.comboBox_reportType, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
		self.connect(self.ui.pushButton_refresh, QtCore.SIGNAL('clicked()'), self.updateData)
		
	
		
	def mkQuery(self):
		"""return the query"""
		reportType = unicode(self.ui.comboBox_reportType.currentText())
		pStart, pEnd = self._getCurrentPeriodStartEnd()
		print pStart, pEnd
		query = """
				select {fields}
				from dienstnehmer, dienste, veranstaltungen
				where 1=1
				and die_dinid = din_id
				and die_verid = ver_id
				and ver_datum between '{pStart}' and '{pEnd}'
				group by {groupByFields}
				"""
				
		if reportType == u'Jährlich':
			fields = 'din_name, sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600+die_pause), count(*)'
			groupByFields = 'din_id, din_name'
		elif reportType == u'Monatlich':
			fields = 'monthname(ver_datum), din_name, sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600+die_pause), count(*)'
			groupByFields = 'monthname(ver_datum), din_id, din_name'
		else:
			fields = 'ver_bezeichnung, ver_datum, din_name, sum((unix_timestamp(die_ende)-unix_timestamp(die_beginn))/3600+die_pause), count(*)'
			groupByFields = 'ver_id, ver_bezeichnung, ver_datum, din_id, din_name'
			
		query = query.format(
							fields=fields,
							groupByFields=groupByFields,
							pStart=pStart.strftime('%Y-%m-%d %H:%M:%S'), 
							pEnd=pEnd.strftime('%Y-%m-%d %H:%M:%S')
							)
			
		return query
	
