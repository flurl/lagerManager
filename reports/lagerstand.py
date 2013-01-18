# -*- coding: utf-8 -*-
import time
import datetime
import copy
from sets import Set

from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.lagerstandReport_gui import Ui_Lagerstand
from graphicsReport import GraphicsReport



class LagerstandReport(GraphicsReport):
	uiClass = Ui_Lagerstand
	ident = 'lagerstand'
	
	def __init__(self, parent=None):
		GraphicsReport.__init__(self, parent)
		
		nop = lambda x: x
		me = self
		dateFunc = lambda day: unicode(day) + ' - ' + (datetime.datetime(int(me.getCurrPeriode()), 1, 1) + datetime.timedelta(int(day) - 1)).strftime('%d.%m.%Y')
		formatter = [nop, dateFunc, nop]
		
		self.setDataFormatter(formatter)
		self.updateData()
		
		
	def setupUi(self):
		super(LagerstandReport, self).setupUi()
		
		self.connect(self.ui.pushButton_refresh, QtCore.SIGNAL('clicked()'), self._onRefreshBtnClicked)
		self.connect(self.ui.lineEdit_filterArticles, QtCore.SIGNAL('textChanged (const QString&)'), self._onArticleFilterChanged)
		
	def updateData(self):
		self.negativeArticles = Set()
		days = []
		for i in range(370):
			days.append({})
		
		query =  self.mkInvQuery()
		results = self.db.exec_(query)
		print query
		print results.lastError().databaseText()
		days[0] = {}
		while results.next():
			name = unicode(results.value(0).toString())
			amount = results.value(1).toFloat()[0]
			days[0][name] = amount
			
			
		query = self.mkConsQuery()
		results = self.db.exec_(query)
		print query
		print results.lastError().databaseText()
		while results.next():
			ckpId = results.value(0).toInt()[0]
			ckpInfo = results.value(1).toString()
			article = unicode(results.value(2).toString())
			amount = results.value(3).toFloat()[0]
			count = results.value(4).toInt()[0]
			
			yday = time.strptime(ckpInfo, '%d.%m.%Y').tm_yday

			days[yday][article] = days[yday].get(article, 0.0) + amount*-1.0
			
			
		query = self.mkDelQuery()
		results = self.db.exec_(query)
		print query
		print results.lastError().databaseText()
		while results.next():
			date = results.value(0).toDateTime().toPyDateTime()
			article = unicode(results.value(1).toString())
			amount = results.value(2).toFloat()[0]
			
			
			yday = date.timetuple().tm_yday
			
			days[yday][article] = days[yday].get(article, 0.0) + amount
		
		dp = {}
		allArticles = set()
		for i in range(len(days)):
			articles = days[i]
			allArticles.update(articles.keys())

		for i in range(len(days)):
			dp[i] = {}
			articles = days[i]
			for article in allArticles:
				if i == 0:
					dp[i][article] = articles.get(article, 0.0)
				else:
					#print 'adding', i, articles.get(article, 0.0)
					dp[i][article] = dp[i-1].get(article, 0.0) + articles.get(article, 0.0)
				if dp[i][article] < 0.0:
					self.negativeArticles.add(article)
		
		#print dp
		self.dp = copy.deepcopy(dp)
		
		self.populateArticleSelection(allArticles)
		self.setDatapoints(dp)
		self.plot()
		
		
		
	def setDatapoints(self, dp):
		activeArticles = []
		for cb in self.articleCheckboxes:
			if cb.isChecked():
				#print 'active:', unicode(cb.text())
				activeArticles.append(unicode(cb.text()))
		#print activeArticles, dp
		for i in range(len(dp)):
			for key in dp[i].keys():
				#if key in activeArticles: print key
				if key not in activeArticles:
					try:
						del dp[i][key]
					except KeyError:
						pass
					
		super(LagerstandReport, self).setDatapoints(dp)
		
		
		
	def populateArticleSelection(self, articles):
		self.articleCheckboxes = []
		widget = QtGui.QWidget()
		layout = QtGui.QVBoxLayout()
		
		cb = QtGui.QCheckBox('Alle')
		layout.addWidget(cb)
		self.connect(cb, QtCore.SIGNAL('stateChanged(int)'), self._onCheckAllChanged)
		
		cb = QtGui.QCheckBox('Alle mit negativen Werten')
		layout.addWidget(cb)
		self.connect(cb, QtCore.SIGNAL('stateChanged(int)'), self.onCheckAllNegativeChanged)
		
		for a in sorted(list(articles)):
			cb = QtGui.QCheckBox(a)
			layout.addWidget(cb)
			self.articleCheckboxes.append(cb)
			
		
		widget.setLayout(layout)
		self.ui.scrollArea_articleSelection.setWidget(widget)
		
		
		
	def mkInvQuery(self):
		"""returns the query for the inventory"""
		query = """
			select artikel_bezeichnung, sum(anzahl)
			from artikel_basis, lagerstand
			where 1=1
			and lagerstand.artikel_id = artikel_basis.artikel_id
			and artikel_periode = %(period_id)s
			and lagerstand.periode_id = %(period_id)s
			group by artikel_bezeichnung
		""" % {'period_id': self._getCurrentPeriodId()}
		
		return query
		
		
	def mkConsQuery(self):
		"""returns the query for the consumption"""
		
		query = """
				select checkpoint_id, checkpoint_info, art2.artikel_bezeichnung, sum(detail_absmenge*zutate_menge/lager_einheit_multiplizierer), count(*)
				from artikel_basis as art1, artikel_basis as art2
				left outer join artikel_basis as ept on art2.artikel_bezeichnung = ept.artikel_bezeichnung,
				artikel_zutaten, journal_details, journal_daten, journal_checkpoints, lager_artikel, lager_einheiten
				where 1=1
				and lager_artikel_artikel = art2.artikel_id
				and detail_artikel_text = art1.artikel_bezeichnung
				and zutate_master_artikel = art1.artikel_id
				and zutate_istRezept = 1
				and zutate_artikel = art2.artikel_id
				and detail_journal = daten_rechnung_id
				and daten_checkpoint_tag = checkpoint_id
				and lager_artikel_einheit = lager_einheit_id
				and checkpoint_typ = 1
				and detail_periode = %(period_id)s
				and daten_periode = %(period_id)s
				and checkpoint_periode = %(period_id)s
				and zutate_periode = %(period_id)s
				and art1.artikel_periode = %(period_id)s
				and art2.artikel_periode = %(period_id)s
				and (ept.artikel_periode = %(period_id)s or ept.artikel_periode is null)
				and (lager_artikel_periode = %(period_id)s or lager_artikel_periode is null)
				and lager_einheit_periode = %(period_id)s
				group by checkpoint_id, checkpoint_info, art2.artikel_bezeichnung
				""" % {'period_id': self._getCurrentPeriodId()}
		query += " union all "
		
		query += """
				select checkpoint_id, checkpoint_info, a.artikel_bezeichnung, sum(detail_absmenge), count(*)
				from artikel_basis as a
				left outer join artikel_zutaten
				on zutate_master_artikel = artikel_id
				join journal_details
				on detail_artikel_text = a.artikel_bezeichnung
				left outer join artikel_basis as ept on detail_artikel_text = ept.artikel_bezeichnung,
				journal_daten, journal_checkpoints
				where 1=1
				and zutate_istRezept is null
				and detail_journal = daten_rechnung_id
				and daten_checkpoint_tag = checkpoint_id
				and checkpoint_typ = 1
				and detail_periode = %(period_id)s
				and daten_periode = %(period_id)s
				and checkpoint_periode = %(period_id)s
				and (zutate_periode = %(period_id)s or zutate_periode is null)
				and a.artikel_periode = %(period_id)s
				and (ept.artikel_periode = %(period_id)s or ept.artikel_periode is null)
				group by checkpoint_id, checkpoint_info, a.artikel_bezeichnung
				order by 1
				""" % {'period_id': self._getCurrentPeriodId()}
		#print query
		return query
		
		
	def mkDelQuery(self):
		"""return the query for the deliveries"""
		query = """
				select datum, artikel_bezeichnung, sum(anzahl)
				from artikel_basis, lager_artikel, lieferungen, lieferungen_details, perioden
				where 1=1
				and lager_artikel.lager_artikel_artikel = artikel_basis.artikel_id
				and lager_artikel.lager_artikel_artikel = lieferungen_details.artikel_id
				and lieferungen.lieferung_id = lieferungen_details.lieferung_id
				and artikel_periode = %(period_id)s
				and lager_artikel_periode = %(period_id)s
				and perioden.periode_id = %(period_id)s
				and lieferungen.datum between periode_start and periode_ende
				group by datum, artikel_bezeichnung
		""" % {'period_id': self._getCurrentPeriodId()}
		
		return query
		
	
	def filterArticlesList(self, text):
		for cb in self.articleCheckboxes:
			if unicode(text).upper() in unicode(cb.text()).upper():
				cb.show()
			else:
				cb.hide()

		
	def _onRefreshBtnClicked(self):
		self.setDatapoints(copy.deepcopy(self.dp))
		self.plot()
		
		
	def _onCheckAllChanged(self, state):
		for cb in self.articleCheckboxes:
			cb.setCheckState(state)
			
	
	def onCheckAllNegativeChanged(self, state):
		for cb in self.articleCheckboxes:
			if unicode(cb.text()) in self.negativeArticles:
				cb.setCheckState(state)
			
			
	def _onArticleFilterChanged(self, newText):
		self.filterArticlesList(newText)
		
		
