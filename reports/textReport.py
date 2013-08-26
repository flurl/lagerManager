# -*- coding: utf-8 -*-
import collections
import csv

from PyQt4 import QtCore, QtGui

from reports.reportBase import ReportBase
from ui.reports.defaultTextReport_gui import Ui_DefaultTextReport

class Heading(object):
	def __init__(self, text=u'', level=1):
		self.text = text
		self.level = level
		
	def __unicode__(self):
		return u'<h%(l)s>%(t)s</h%(l)s>' % {'l': self.level, 't': self.text}
	
	def __str__(self):
		return unicode(self).encode('utf-8')
	
class Footer(object):
	def __init__(self, text=u''):
		self.text = text
		
	def __unicode__(self):
		return u'<hr>%(t)s' % {'t': self.text}
	
	def __str__(self):
		return unicode(self).encode('utf-8')


class TextReport(ReportBase):
	uiClass = Ui_DefaultTextReport
	
	def __init__(self, parent):
		ReportBase.__init__(self, parent)
		
		self.__header = u''
		self.__footer = u''
		self.__tableHeaders = []
		self.__repeatTableHeadersAfterBlankLine = False
		
		self.setData([])
		
		
	def setupSignals(self):
		ReportBase.setupSignals(self)
		self.connect(self.ui.pushButton_export, QtCore.SIGNAL('clicked()'), self.exportData)

		
	def setHeader(self, header):
		self.__header = header
		
	def setFooter(self, footer):
		self.__footer = footer
		
	def setTableHeaders(self, headers, repeat=False):
		"""
		@headers a list of table headers
		@repeat defines if the headers should be repeated after each blank line
		"""
		self.__tableHeaders = headers
		self.setTableHeadersRepeat(repeat)
		
	def setTableHeadersRepeat(self, repeat):
		self.__repeatTableHeadersAfterBlankLine = repeat
		
	def setData(self, data):
		"""override this method for custom data set, otherwise supply a query"""
		if isinstance(data, basestring): 
			results = self.db.exec_(data)
			self.__data = []
			while results.next():
				record = results.record()
				self.__data.append([record.value(i).toString() for i in range(record.count())])
		elif isinstance(data, collections.Iterable): 
			self.__data = data
		else:
			raise
		
		
	def process(self):
		elements = []
		elements.append(Heading(self.__header))
		elements.append(self.processData())
		elements.append(Footer(self.__footer))
		
		self.ui.textView.setText(''.join(unicode(e) for e in elements))
		
		
	def processData(self):
		output = u''
		output += u'<table border="1">'
		
		output += self.mkTableHeaders()
		blankLine = False
		
		for row in self.__data:
			output += u'<tr>'
			for cell in row:
				if cell is None:
					output += u'<td>'+u'☭'*10+u'</td>'
					blankLine = True
				else:
					#apply formating
					if type(cell) is list or type(cell) is tuple:
						if cell[1] == 'strong':
							cell = u'<strong>' + unicode(cell[0]) + u'</strong>'
					output += u'<td>%s</td>' % (cell,)
			output += u'</tr>'
			
			if blankLine:
				blankLine = False
				output += self.mkTableHeaders()
				
		output += u'</table>'
		return output
	
	
	def mkTableHeaders(self):
		output = u''
		if len(self.__tableHeaders) > 0:
			output += u'<tr>'
			for h in self.__tableHeaders:
				output += u'<th>%s</th>' % (h, )
			output += u'</tr>'
		return output
	
	def updatePeriod(self, periodId):
		self.updateData()
		self.process()
		
		
	def exportData(self):
		filename = QtGui.QFileDialog.getSaveFileName(self, 'Datei speichern', '', 'CSV Files (*.csv)')
		with open(filename, 'wb') as f:
			writer = csv.writer(f)
			writer.writerows(self.__data)
