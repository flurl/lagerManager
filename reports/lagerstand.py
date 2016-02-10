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
		self.articlesMinimum = {}
		self.articlesMaximum = {}
		
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
		self.connect(self.ui.checkBox_ignorePrefix, QtCore.SIGNAL('stateChanged (int)'), self.updateData)
		
	def updateData(self):
		self.negativeArticles = Set()
		ignorePrefix = self.ui.checkBox_ignorePrefix.isChecked()
		days = []
		markingData = []
		for i in range(370):
			days.append({})
		
		query =  self.mkInvQuery()
		results = self.db.exec_(query)
		#print query
		#print results.lastError().databaseText()
		days[0] = {}
		while results.next():
			name = unicode(results.value(0).toString())
			if ignorePrefix and u'-' in name:
				name = name.partition(u'-')[2]
			amount = results.value(1).toFloat()[0]
			days[0][name] = days[0].get(name, 0.0) + amount
			
			
		query = self.mkConsQuery()
		results = self.db.exec_(query)
		#print query
		#print results.lastError().databaseText()
		while results.next():
			ckpId = results.value(0).toInt()[0]
			ckpInfo = results.value(1).toString()
			article = unicode(results.value(2).toString())
			if ignorePrefix and u'-' in article:
				article = article.partition(u'-')[2]
			
			amount = results.value(3).toFloat()[0]
			count = results.value(4).toInt()[0]
			
			date = time.strptime(ckpInfo, '%d.%m.%Y')
			yday = date.tm_yday
			if str(date.tm_year) != self.getCurrPeriode():
				continue

			days[yday][article] = days[yday].get(article, 0.0) + amount*-1.0
			
			
		query = self.mkDelQuery()
		results = self.db.exec_(query)
		#print query
		#print results.lastError().databaseText()
		while results.next():
			date = results.value(0).toDateTime().toPyDateTime()
			article = unicode(results.value(1).toString())
			if ignorePrefix and u'-' in article:
				article = article.partition(u'-')[2]
				
			amount = results.value(2).toFloat()[0]
			
			
			yday = date.timetuple().tm_yday
			
			days[yday][article] = days[yday].get(article, 0.0) + amount
		
		dp = {}
		allArticles = set()
		for i in range(len(days)):
			articles = days[i]
			allArticles.update(articles.keys())
		
		extraData = {}
		self.articlesMinimum = {}
		self.articlesMaximum = {}
		for i in range(len(days)):
			dp[i] = {}
			articles = days[i]
			day = (datetime.datetime(int(self.getCurrPeriode()), 1, 1) + datetime.timedelta(int(i) - 1))
			markingData.append(day.strftime('%d.%m.%Y'))
			
			deliveries = self.getDeliveryForDay(day)
			if deliveries is None:
				deliveries = []
			
			extraData[i] = {}
			
			for article in allArticles:
				extraData[i][article] = deliveries
				if i == 0:
					dp[i][article] = articles.get(article, 0.0)
				else:
					#print 'adding', i, articles.get(article, 0.0)
					dp[i][article] = dp[i-1].get(article, 0.0) + articles.get(article, 0.0)
				if dp[i][article] < 0.0:
					self.negativeArticles.add(article)
				if (not article in self.articlesMinimum) or (dp[i][article] < self.articlesMinimum[article]):
					self.articlesMinimum[article] = dp[i][article]
				elif (not article in self.articlesMaximum) or (dp[i][article] > self.articlesMaximum[article]):
					self.articlesMaximum[article] = dp[i][article]
					
				
		
		#print dp
		self.dp = copy.deepcopy(dp)
		
		self.populateArticleSelection(allArticles)
		self.setDatapoints(dp)
		self.setMarkingData(markingData)
		self.setExtraData(extraData)
		self.plot()
		
		
		
	def setDatapoints(self, dp):
		activeArticles = []
		modifiers = []
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
				else:
					mod = unicode(self.articleMods[key][0].text())
					if mod != u'':
						dp[i][key] += float(mod)
					
					
		super(LagerstandReport, self).setDatapoints(dp)
		
		
		
	def populateArticleSelection(self, articles):
		self.articleCheckboxes = []
		self.articleMods = {}
		widget = QtGui.QWidget()
		layout = QtGui.QVBoxLayout()
		
		cb = QtGui.QCheckBox('Alle')
		layout.addWidget(cb)
		self.connect(cb, QtCore.SIGNAL('stateChanged(int)'), self._onCheckAllChanged)
		
		cb = QtGui.QCheckBox('Mit negativen Werten hevorheben')
		layout.addWidget(cb)
		self.connect(cb, QtCore.SIGNAL('stateChanged(int)'), self.onCheckAllNegativeChanged)
		
		for a in sorted(list(articles)):
			containerWidget = QtGui.QWidget()
			vl = QtGui.QVBoxLayout()
			cb = QtGui.QCheckBox(a)
			vl.addWidget(cb, 0)
			try:
				min_ = self.articlesMinimum[a]
				max_ = self.articlesMaximum[a]
				label = QtGui.QLabel(unicode(round(min_, 2))+u' - '+unicode(round(max_,2)))
				vl.addWidget(label)
			except KeyError:
				pass
			
			lineEdit = QtGui.QLineEdit()
			vl.addWidget(lineEdit, 0)
			lineEdit.hide()
			
			containerWidget.setLayout(vl)
			layout.addWidget(containerWidget)
			
			func = lambda i, le=lineEdit: le.show()
			self.connect(cb, QtCore.SIGNAL('stateChanged (int)'), func)
			
			self.articleCheckboxes.append(cb)
			self.articleMods[a] = (lineEdit, ) #we use a tuple, perhaps somewhen additional modifiers are needed (perhaps a start date for the modifiers or so)
			
		
		widget.setLayout(layout)
		self.ui.scrollArea_articleSelection.setWidget(widget)
		
		#adjust line edits width
		#for key, mod in self.articleMods.iteritems():
		#	le = mod[0]
		#	le.setFixedSize(50, lineEdit.height())
		
		
		
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
				select checkpoint_id, checkpoint_info, art2.artikel_bezeichnung, sum(tisch_bondetail_absmenge*zutate_menge/lager_einheit_multiplizierer), count(*)
				from artikel_basis as art1, artikel_basis as art2
				left outer join artikel_basis as ept on art2.artikel_id = ept.artikel_id,
				artikel_zutaten, tische_aktiv, tische_bons, tische_bondetails, journal_checkpoints, lager_artikel, lager_einheiten
				where 1=1
				and lager_artikel_artikel = art2.artikel_id
				and tisch_bondetail_artikel = art1.artikel_id
				and zutate_master_artikel = art1.artikel_id
				and zutate_istRezept = 1
				and zutate_artikel = art2.artikel_id
				and tisch_bondetail_bon = tisch_bon_id
				and tisch_bon_tisch = tisch_id
				and checkpoint_tag = checkpoint_id
				and lager_artikel_einheit = lager_einheit_id
				and checkpoint_typ = 1
				and tisch_periode = %(period_id)s
				and tisch_bon_periode = %(period_id)s
				and tisch_bondetail_periode = %(period_id)s
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
				select checkpoint_id, checkpoint_info, a.artikel_bezeichnung, sum(tisch_bondetail_absmenge), count(*)
				from artikel_basis as a
				left outer join artikel_zutaten
				on zutate_master_artikel = artikel_id
				join tische_bondetails
				on tisch_bondetail_artikel = a.artikel_id
				left outer join artikel_basis as ept on tisch_bondetail_artikel = ept.artikel_id,
				journal_checkpoints, tische_aktiv, tische_bons
				where 1=1
				and zutate_istRezept is null
				and tisch_id = tisch_bon_tisch
				and tisch_bondetail_bon = tisch_bon_id
				and checkpoint_tag = checkpoint_id
				and checkpoint_typ = 1
				and tisch_periode = %(period_id)s
				and tisch_bon_periode = %(period_id)s
				and tisch_bondetail_periode = %(period_id)s
				and checkpoint_periode = %(period_id)s
				and (zutate_periode = %(period_id)s or zutate_periode is null)
				and a.artikel_periode = %(period_id)s
				and (ept.artikel_periode = %(period_id)s or ept.artikel_periode is null)
				group by checkpoint_id, checkpoint_info, a.artikel_bezeichnung
				order by 1
				""" % {'period_id': self._getCurrentPeriodId()}
		print query
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
		
		
	def getDeliveryForDay(self, day):
		day = QtCore.QDateTime(day)
		query = QtSql.QSqlQuery()
		query.prepare("select lieferung_id, if(lie_ist_verbrauch = 0, 'Lieferung', 'Verbrauch'), lieferant_name from lieferungen, lieferanten where date(datum) = date(?) and lieferungen.lieferant_id = lieferanten.lieferant_id")
		query.addBindValue(day)
		query.exec_()
		if query.lastError().isValid():
			print "Error while selecting lieferungen for day %s"%(day, ), query.lastError().text()
			return None
		
		if query.size() == 0:
			return None
		
		deliveries = []
		while query.next():
			delId = unicode(query.value(0).toString())
			consOrDel = unicode(query.value(1).toString())
			name = unicode(query.value(2).toString())
			deliveries.append(u'ID: ' + delId + '-' + consOrDel + '-' + name)
			
		return deliveries
			
		
		
	
	def filterArticlesList(self, text):
		for cb in self.articleCheckboxes:
			parent = cb.parent()
			if unicode(text).upper() in unicode(cb.text()).upper():
				parent.show()
			else:
				parent.hide()

		
	def _onRefreshBtnClicked(self):
		self.setDatapoints(copy.deepcopy(self.dp))
		self.plot()
		
		
	def _onCheckAllChanged(self, state):
		for cb in self.articleCheckboxes:
			cb.setCheckState(state)
			
	
	def onCheckAllNegativeChanged(self, state):
		for cb in self.articleCheckboxes:
			for art in self.negativeArticles:
				if unicode(cb.text()).startswith(art):
					if state == QtCore.Qt.Checked:
						ss = "QCheckBox {color: red; background-color: #fff;}"
					#cb.setCheckState(state)
					else:
						ss = self.ui.checkBox_ignorePrefix.styleSheet()
						
					cb.setStyleSheet(ss)
			
			
	def _onArticleFilterChanged(self, newText):
		self.filterArticlesList(newText)
		
		
