# -*- coding: utf-8 -*-
#import time
#import copy
from sets import Set

from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.verprobungReport_gui import Ui_Verprobung
from textReport import TextReport

articleGroupRole = QtCore.Qt.UserRole+1


class VerprobungReport(TextReport):
	uiClass = Ui_Verprobung
	ident = 'verprobung'
	
	def __init__(self, parent=None):
		TextReport.__init__(self, parent)
				
		self.setHeader('Verprobung')
		self.setFooter('Alle Preise netto')
		
		self.setupWidgets()
		#self.updateData()
		
	def setupUi(self):
		super(VerprobungReport, self).setupUi()
		
		self.ui.treeView_purchasesArticleGroups.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.ui.treeView_salesArticleGroups.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		
	def setupSignals(self):
		super(VerprobungReport, self).setupSignals()
		self.connect(self.ui.pushButton_purchasesCheckAll, QtCore.SIGNAL('clicked()'), self.checkPurchasesArticles)
		self.connect(self.ui.pushButton_purchasesUncheckAll, QtCore.SIGNAL('clicked()'), self.uncheckPurchasesArticles)
		self.connect(self.ui.checkBox_purchasesFilter, QtCore.SIGNAL('stateChanged (int)'), self.filterPurchasesArticles)
		self.connect(self.ui.lineEdit_purchasesFilter, QtCore.SIGNAL('textEdited (const QString&)'), lambda string: self.filterStringUpdated(string, self.ui.listView_purchasesArticles.model()))
		
		self.connect(self.ui.pushButton_salesCheckAll, QtCore.SIGNAL('clicked()'), self.checkSalesArticles)
		self.connect(self.ui.pushButton_salesUncheckAll, QtCore.SIGNAL('clicked()'), self.uncheckSalesArticles)
		self.connect(self.ui.checkBox_salesFilter, QtCore.SIGNAL('stateChanged (int)'), self.filterSalesArticles)
		self.connect(self.ui.lineEdit_salesFilter, QtCore.SIGNAL('textEdited (const QString&)'), lambda string: self.filterStringUpdated(string, self.ui.listView_salesArticles.model()))
		
		self.connect(self.ui.pushButton_refresh, QtCore.SIGNAL('clicked()'), self.updateData)
		
		
		
	def setupWidgets(self):
		groupsModel = QtGui.QStandardItemModel()
		tree = self.getArticleGroupsTree()
		rootItem = groupsModel.invisibleRootItem()
		rootItem.appendRows(tree)
		self.ui.treeView_purchasesArticleGroups.setModel(groupsModel)
		
		salesGroupsModel = QtGui.QStandardItemModel()
		tree = self.getJournalArticleGroups()
		rootItem = salesGroupsModel.invisibleRootItem()
		rootItem.appendRows(tree)
		self.ui.treeView_salesArticleGroups.setModel(salesGroupsModel)
		
		articles = self.getArticlesList()
		purchasesArticlesModel = QtGui.QStandardItemModel()
		for article in articles:
			purchasesArticlesModel.appendRow(article)
		purchasesArticlesProxyModel = QtGui.QSortFilterProxyModel()
		purchasesArticlesProxyModel.setSourceModel(purchasesArticlesModel)
		self.ui.listView_purchasesArticles.setModel(purchasesArticlesProxyModel)
		
		
		articles = self.getJournalArticlesList()
		salesArticlesModel = QtGui.QStandardItemModel()
		for article in articles:
			salesArticlesModel.appendRow(article)
		salesArticlesProxyModel = QtGui.QSortFilterProxyModel()
		salesArticlesProxyModel.setSourceModel(salesArticlesModel)
		self.ui.listView_salesArticles.setModel(salesArticlesProxyModel)
		
				
		
		
	def updateData(self):
		data = []
		purchaseArticles = self.getSelectedPurchaseArticles()
		salesArticles = self.getSelectedSalesArticles()

		print purchaseArticles
		print salesArticles
		
		pStart, pEnd = self._getCurrentPeriodStartEnd()
		query = """
				select artikel_bezeichnung, sum(liedet.anzahl*liedet.einkaufspreis)
				from lieferungen_details as liedet, lieferungen as lie, artikel_basis as ab
				where 1=1
				and lie.lieferung_id = liedet.lieferung_id
				and liedet.artikel_id = ab.artikel_id
				and lie.datum between '%s' and '%s'
				and liedet.artikel_id in (%s)
				and artikel_periode = %s
				group by ab.artikel_id, ab.artikel_bezeichnung
				""" % (pStart, pEnd, ', '.join(map(unicode, purchaseArticles)), self._getCurrentPeriodId())

		print query
		results = self.db.exec_(query)
		if results.lastError().isValid():
			print 'Error while selecting purchase sum'
			return
		else:
			purchaseTotal = 0.0
			while results.next():
				article = results.value(0).toString()
				sum_ = results.value(1).toFloat()[0]
				data.append([article, round(sum_, 2)])
				purchaseTotal += sum_
				
			data.append([['Einkauf gesamt', 'strong'], [round(purchaseTotal, 2), 'strong']])
			
		data.append([None, None])
		
		
		query = """
				select detail_artikel_text, sum(detail_absmenge*detail_preis/(detail_mwst/100+1))
				from journal_details
				where 1=1
				and detail_istUmsatz = 1
				and detail_artikel_text in (%s)
				and detail_periode = %s
				group by detail_artikel_text
				""" % (', '.join(map(lambda x: "'%s'"%x, salesArticles)), self._getCurrentPeriodId())

		print query
		results = self.db.exec_(query)
		if results.lastError().isValid():
			print 'Error while selecting sales sum'
			return
		else:
			salesTotal = 0.0
			while results.next():
				article = unicode(results.value(0).toString())
				sum_ = results.value(1).toFloat()[0]
				data.append([article, round(sum_, 2)])
				salesTotal += sum_
				
			data.append([['Verkauf gesamt', 'strong'], [round(salesTotal, 2), 'strong']])
			
		data.append([None, None])
		
		try:
			factor = salesTotal/purchaseTotal
		except ZeroDivisionError:
			factor = 0.0
		
		data.append([[u'Verhältnis', 'strong'], [round(factor, 2), 'strong']])
		
		self.setData(data)
		self.process()
		
		
	def getArticleGroupsTree(self, parent=None):
		print parent
		#tree = QtGui.QStandardItem()
		row = []
		
		query = """
				select artikel_gruppe_id, artikel_gruppe_parent_id, artikel_gruppe_name
				from artikel_gruppen
				where 1=1
				and artikel_gruppe_parent_id %s
				and artikel_gruppe_periode = %s
				""" % ("is null" if parent is None else "= %s"%(parent,), self._getCurrentPeriodId())
		
		results = self.db.exec_(query)
		print query
		if results.lastError().isValid():
			print 'Error while selecting artikel_gruppen hierarchy'
		else:
			while results.next():
				gruppenId, ok = results.value(0).toInt()
				parentId, ok = results.value(1).toInt()
				name = results.value(2).toString()
				
				item = QtGui.QStandardItem(unicode(name))
				item.setData(gruppenId)
				
				nextLevel = self.getArticleGroupsTree(gruppenId)
				if len(nextLevel) > 0:
					item.appendRows(nextLevel)
				
				row.append(item) 
				QtGui
				
		return row
			
			
	def getArticlesList(self):
		articles = []
		query = QtSql.QSqlQuery()
		query.prepare("""
						select artikel_id, artikel_bezeichnung, artikel_gruppe
						from artikel_basis
						where 1=1
						and artikel_periode = ?
						order by artikel_gruppe, artikel_bezeichnung""")
		query.addBindValue(self._getCurrentPeriodId())
		query.exec_()

		if query.lastError().isValid():
			print 'Error while selecting artikel'
		else:
			while query.next():
				artikelId, ok = query.value(0).toInt()
				bezeichnung = query.value(1).toString()
				artikelGruppe, ok = query.value(2).toInt()
				
				item = QtGui.QStandardItem(unicode(bezeichnung))
				item.setData(artikelGruppe, articleGroupRole)
				item.setData(artikelId, QtCore.Qt.UserRole+2)
				item.setCheckable(True)
				item.setCheckState(QtCore.Qt.Unchecked)
				
				articles.append(item)
				
		return articles
				
				
	def getJournalArticleGroups(self):
		"""selects and parses all article groups from the journal"""
		
		groups = {}
		
		query = QtSql.QSqlQuery()
		query.prepare("""
						select distinct detail_gruppe
						from journal_details
						where 1=1
						and detail_periode = ?
						order by detail_gruppe
						""")
		query.addBindValue(self._getCurrentPeriodId())
		query.exec_()

		if query.lastError().isValid():
			print 'Error while selecting artikel gruppen from journal_details'
		else:
			while query.next():
				gs = groupString = unicode(query.value(0).toString())
				
				groupHierarchy = []
				
				while len(groupString) > 0:
					index = groupString.find('$')
					charCount = int(groupString[1:index])
					group = groupString[index+1:index+1+charCount]
					groupHierarchy.append(group)
					
					groupString = groupString[index+1+charCount:]
					
				groups[gs] = groupHierarchy
		
		print groups
		
		row = []
		for gs in sorted(groups.keys()):
			item = QtGui.QStandardItem(u'->'.join(groups[gs]))
			item.setData(gs, articleGroupRole)
			row.append(item)
			
		return row
	
	def getJournalArticlesList(self):
		articles = []
		query = QtSql.QSqlQuery()
		query.prepare("""
						select distinct detail_artikel_text, detail_gruppe
						from journal_details
						where 1=1
						and detail_periode = ?
						order by detail_gruppe, detail_artikel_text""")
		query.addBindValue(self._getCurrentPeriodId())
		query.exec_()

		if query.lastError().isValid():
			print 'Error while selecting artikel from journal_details'
		else:
			while query.next():
				bezeichnung = query.value(0).toString()
				artikelGruppe = query.value(1).toString()
				
				item = QtGui.QStandardItem(unicode(bezeichnung))
				item.setData(artikelGruppe, articleGroupRole)
				item.setCheckable(True)
				item.setCheckState(QtCore.Qt.Unchecked)
				
				articles.append(item)
				
		return articles
	
	
	def getSelectedPurchaseArticles(self):
		articles = []
		model = self.ui.listView_purchasesArticles.model().sourceModel()
		
		for rowNum in range(model.rowCount()):
			item = model.item(rowNum, 0)
			if item.checkState() == QtCore.Qt.Checked:
				articles.append(item.data(QtCore.Qt.UserRole+2).toInt()[0])
				
		return articles
				
				
	def getSelectedSalesArticles(self):
		articles = []
		model = self.ui.listView_salesArticles.model().sourceModel()
		
		for rowNum in range(model.rowCount()):
			item = model.item(rowNum, 0)
			if item.checkState() == QtCore.Qt.Checked:
				articles.append(unicode(item.data(QtCore.Qt.DisplayRole).toString()))
				
		return articles
	
		
	def checkPurchasesArticles(self):
		self.changeCheckState(QtCore.Qt.Checked, self.ui.treeView_purchasesArticleGroups, self.ui.listView_purchasesArticles)
	
	def uncheckPurchasesArticles(self):
		self.changeCheckState(QtCore.Qt.Unchecked, self.ui.treeView_purchasesArticleGroups, self.ui.listView_purchasesArticles)
	
	def filterPurchasesArticles(self, state):
		print "filtering purchase articles"
		self.filterArticles(state, self.ui.treeView_purchasesArticleGroups, self.ui.listView_purchasesArticles)
			
	
	def checkSalesArticles(self):
		self.changeCheckState(QtCore.Qt.Checked, self.ui.treeView_salesArticleGroups, self.ui.listView_salesArticles)
	
	def uncheckSalesArticles(self):
		self.changeCheckState(QtCore.Qt.Unchecked, self.ui.treeView_salesArticleGroups, self.ui.listView_salesArticles)
	
	def filterSalesArticles(self, state):
		print "filtering sales articles"
		self.filterArticles(state, self.ui.treeView_salesArticleGroups, self.ui.listView_salesArticles)
		
		
	
	def changeCheckState(self, state, groupsWidget, articlesWidget):
		print "changeCheckState"
		selectedIndexes = groupsWidget.selectionModel().selectedIndexes()
		groupsModel = groupsWidget.model()
		
		selectedGroups = []
		for idx in selectedIndexes:
			#print groupsModel.data(idx).toString()
			selectedGroups.append(groupsModel.data(idx, articleGroupRole).toString())
		
		print "changeCheckState; groups:", selectedGroups
		
		articlesModel = articlesWidget.model().sourceModel()
		for rowNum in range(articlesModel.rowCount()):
			item = articlesModel.item(rowNum, 0)
			#print u"changeCheckState loop; item:", item, u'item data:', item.data(articleGroupRole).toInt(), item.data().toString()
			if item.data(articleGroupRole).toString() in selectedGroups:
				print "changeCheckState if"
				item.setCheckState(state)
				
				
	def filterArticles(self, state, groupsWidget, articlesWidget):
		if state == QtCore.Qt.Checked:
			#groupsWidget = self.ui.treeView_salesArticleGroups
			selectedIndexes = groupsWidget.selectionModel().selectedIndexes()
			groupsModel = groupsWidget.model()
			
			selectedGroups = []
			for idx in selectedIndexes:
				#print groupsModel.data(idx).toString()
				selectedGroups.append(groupsModel.data(idx, articleGroupRole).toString())
			
			print "filterSalesArticles groups:", selectedGroups
			
			regExp = QtCore.QRegExp('%s'%'|'.join(map(unicode, map(QtCore.QRegExp.escape, selectedGroups))))
			print "regExp:", '|'.join(map(unicode, map(QtCore.QRegExp.escape, selectedGroups)))
		else:
			regExp = QtCore.QRegExp('')
	
		#articlesWidget = self.ui.listView_salesArticles
		articlesProxyModel = articlesWidget.model()
		articlesProxyModel.setFilterRole(articleGroupRole)
		
		articlesProxyModel.setFilterRegExp(regExp)
			
			
	def filterStringUpdated(self, string, model):
		model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
		model.setFilterFixedString(string)
		
	def updatePeriod(self, p):
		self.setupWidgets()
		super(VerprobungReport, self).updatePeriod(p)
		
		
	