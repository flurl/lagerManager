# -*- coding: utf-8 -*-
"""




from graphicsReport import GraphicsReport"""
import time
import datetime
import copy

from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.verbrauchReport_gui import Ui_Verbrauch
from lagerstand import LagerstandReport



class VerbrauchReport(LagerstandReport):
	uiClass = Ui_Verbrauch
	ident = 'verbrauch'
	
	def __init__(self, parent=None):
		LagerstandReport.__init__(self, parent)
	
	#def setupUi(self):
		#self.ui = Ui_Verbrauch()
		#self.ui.setupUi(self)
		
		#self.connect(self.ui.pushButton_refresh, QtCore.SIGNAL('clicked()'), self._onRefreshBtnClicked)
		#self.connect(self.ui.lineEdit_filterArticles, QtCore.SIGNAL('textChanged (const QString&)'), self._onArticleFilterChanged)
		
	def updateData(self):
		days = []
		for i in range(366):
			days.append({})
			
		query = self.mkConsQuery()
		results = self.db.exec_(query)

		while results.next():
			ckpId = results.value(0).toInt()[0]
			ckpInfo = results.value(1).toString()
			article = unicode(results.value(2).toString())
			amount = results.value(3).toFloat()[0]
			count = results.value(4).toInt()[0]
			
			yday = time.strptime(ckpInfo, '%d.%m.%Y').tm_yday

			days[yday][article] =  days[yday].get(article, 0.0) + amount
		
		dp = {}
		allArticles = set()
		for i in range(len(days)):
			dp[i] = {}
			articles = days[i]
			allArticles.update(articles.keys())
			for article in allArticles:
				if i == 0:
					dp[i][article] = articles.get(article, 0.0)
				else:
					#print 'adding', i, articles.get(article, 0.0)
					dp[i][article] = dp[i-1].get(article, 0.0) + articles.get(article, 0.0)
		
		#all articles must exist for each and every day
		for i in range(len(days)):
			for article in allArticles:
				if article not in dp[i]:
					dp[i][article] = 0.0
		
		#print dp
		self.dp = copy.deepcopy(dp)
		
		self.populateArticleSelection(allArticles)
		self.setDatapoints(dp)
		self.plot()
		
