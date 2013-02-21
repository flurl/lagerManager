# -*- coding: utf-8 -*-
import collections

from PyQt4 import QtCore

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
		self.setHeader('')
		self.setFooter('')
		self.setData([])

		
	def setHeader(self, header):
		self.header = header
		
	def setFooter(self, footer):
		self.footer = footer
		
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
		elements.append(Heading(self.header))
		elements.append(self.processData())
		elements.append(Footer(self.footer))
		
		self.ui.textView.setText(''.join(unicode(e) for e in elements))
		
		
	def processData(self):
		output = u''
		output += u'<table border="1">'
		for row in self.__data:
			output += u'<tr>'
			for cell in row:
				if cell is None:
					output += u'<td>'+u'☭'*10+u'</td>'
				else:
					#apply formating
					if type(cell) is list or type(cell) is tuple:
						if cell[1] == 'strong':
							cell = u'<strong>' + unicode(cell[0]) + u'</strong>'
					output += u'<td>%s</td>' % (cell,)
			output += u'</tr>'
		output += u'</table>'
		return output
	
	def updatePeriod(self, periodId):
		self.updateData()
		self.process()
