# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection
import config

from forms.formBase import FormBase
from ui.forms.lagerartikelAuswahlForm_gui import Ui_LagerartikelAuswahlForm
import config

class LagerartikelAuswahlForm(FormBase):
	
	uiClass = Ui_LagerartikelAuswahlForm
	ident = 'lagerartikelAuswahl'
	
	def __init__(self, parent):
		super(LagerartikelAuswahlForm, self).__init__(parent)
		
	
	def setupUi(self):
		super(LagerartikelAuswahlForm, self).setupUi()
		
		
	def setupSignals(self):
		self.connect(self.ui.comboBox_period, QtCore.SIGNAL('currentIndexChanged(int)'), self.setupArticleTable)
		super(LagerartikelAuswahlForm, self).setupSignals()
		self.connect(self.ui.pushButton_checkAll, QtCore.SIGNAL('clicked()'), self.checkArtikelGruppe)
		self.connect(self.ui.pushButton_uncheckAll, QtCore.SIGNAL('clicked()'), self.uncheckArtikelGruppe)
		self.connect(self.ui.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)
		self.connect(self.ui.buttonBox, QtCore.SIGNAL('rejected()'), self.reject)
		
		
	
	def setupArticleTable(self):
		self.populateTable()
		self.populateGruppenCombobox()
	
	
	def populateTable(self):
		try:
			excludeArticles = config.config['connection'][DBConnection.connName]['period'][unicode(self.getCurrentPeriodId())]['exclude_articles']
		except KeyError:
			excludeArticles = []
		
		#in the config they are saved as strings
		excludeArticles = [int(a) for a in excludeArticles]
		
		self.ui.tableWidget_lagerartikel.setRowCount(0)
		self.ui.tableWidget_lagerartikel.setColumnCount(4)
		self.ui.tableWidget_lagerartikel.hideColumn(0)
		self.ui.tableWidget_lagerartikel.hideColumn(1)
		
		query = QtSql.QSqlQuery()
		query.prepare("""
						select lager_artikel_artikel, artikel_bezeichnung, artikel_gruppe, artikel_gruppe_name
						from lager_artikel, artikel_basis, artikel_gruppen
						where 1=1
						and artikel_gruppe_id = artikel_gruppe
						and lager_artikel_artikel = artikel_id
						and artikel_gruppe_periode = ?
						and lager_artikel_periode = ?
						and artikel_periode = ?""")
		query.addBindValue(self.getCurrentPeriodId())
		query.addBindValue(self.getCurrentPeriodId())
		query.addBindValue(self.getCurrentPeriodId())
		query.exec_()

		if query.lastError().isValid():
			print 'Error while selecting lagerartikel'
		else:
			while query.next():
				artikelId, ok = query.value(0).toInt()
				bezeichnung = query.value(1).toString()
				artikelGruppe, ok = query.value(2).toInt()
				artikelGruppeName = query.value(3).toString()
				
				newRow = self.ui.tableWidget_lagerartikel.rowCount()
				self.ui.tableWidget_lagerartikel.insertRow(newRow)
				
				tabWidget = QtGui.QTableWidgetItem(unicode(artikelId))
				self.ui.tableWidget_lagerartikel.setItem(newRow, 0, tabWidget)
				
				tabWidget = QtGui.QTableWidgetItem(unicode(artikelGruppe))
				self.ui.tableWidget_lagerartikel.setItem(newRow, 1, tabWidget)
				
				tabWidget = QtGui.QTableWidgetItem(unicode(bezeichnung, 'iso8859-1'))
				tabWidget.setFlags(QtCore.Qt.ItemFlag(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled))
				#if self._parent.activeArticles is None or bezeichnung in self._parent.activeArticles: checkState = QtCore.Qt.Checked
				#else: checkState = QtCore.Qt.Unchecked
				checkState = QtCore.Qt.Checked if artikelId in excludeArticles else QtCore.Qt.Unchecked
				tabWidget.setCheckState(checkState)
				
				self.ui.tableWidget_lagerartikel.setItem(newRow, 2, tabWidget)
				
				tabWidget = QtGui.QTableWidgetItem(unicode(artikelGruppeName, 'iso8859-1'))
				self.ui.tableWidget_lagerartikel.setItem(newRow, 3, tabWidget)
				


	def populateGruppenCombobox(self):
		self.artikelGruppenModel = QtSql.QSqlTableModel()
		self.artikelGruppenModel.setTable('artikel_gruppen')
		#self.artikelGruppenModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		where = """
				artikel_gruppe_id in (
				select artikel_gruppe 
				from lager_artikel, artikel_basis 
				where 1=1
				and lager_artikel_artikel = artikel_id
				and lager_artikel_periode = %(perId)s
				and artikel_periode = %(perId)s)
				and artikel_gruppe_periode = %(perId)s""" % {'perId':self.getCurrentPeriodId()}
				
		
		self.artikelGruppenModel.setFilter(where)
		self.artikelGruppenModel.select()
		
		self.ui.comboBox_artikelGruppen.setModel(self.artikelGruppenModel)
		self.ui.comboBox_artikelGruppen.setModelColumn(self.artikelGruppenModel.fieldIndex('artikel_gruppe_name'))
		
		
	def checkArtikelGruppe(self):
		state = QtCore.Qt.Checked
		self.updateArtikelGruppeStatus(state)
		
		
	def uncheckArtikelGruppe(self):
		state = QtCore.Qt.Unchecked
		self.updateArtikelGruppeStatus(state)
		
		
	def updateArtikelGruppeStatus(self, checkState):
		gruppeId = self.getCurrentArtikelGruppeId()
		#vals = []
		for i in range(0, self.ui.tableWidget_lagerartikel.rowCount()):
			if self.ui.tableWidget_lagerartikel.item(i, 1).text() == unicode(gruppeId): 
				self.ui.tableWidget_lagerartikel.item(i, 2).setCheckState(checkState)
		
		
	def getCurrentArtikelGruppeId(self):
		row = self.ui.comboBox_artikelGruppen.currentIndex()
		col = self.artikelGruppenModel.fieldIndex('artikel_gruppe_id')
		index = self.artikelGruppenModel.index(row, col)
		artikelGruppeId = self.artikelGruppenModel.data(index).toInt()[0]
		return artikelGruppeId
	
	def accept(self):
		tw = self.ui.tableWidget_lagerartikel
		articleIds = []
		for i in range(0, tw.rowCount()):
			if tw.item(i, 2).checkState() == QtCore.Qt.Checked: 
				articleIds.append(int(tw.item(i, 0).text()))
		
		try:
			tmp = config.config['connection']
		except KeyError:
			config.config['connection'] = {}
			
		try:
			tmp = config.config['connection'][DBConnection.connName]
		except KeyError:
			config.config['connection'][DBConnection.connName] = {}
			
		try:
			tmp = config.config['connection'][DBConnection.connName]['period']
		except KeyError:
			config.config['connection'][DBConnection.connName]['period'] = {}
			
		try:
			tmp = config.config['connection'][DBConnection.connName]['period'][unicode(self.getCurrentPeriodId())]
		except KeyError:
			config.config['connection'][DBConnection.connName]['period'][unicode(self.getCurrentPeriodId())] = {}
			
		config.config['connection'][DBConnection.connName]['period'][unicode(self.getCurrentPeriodId())]['exclude_articles'] = articleIds
		config.config.write()
		
		super(LagerartikelAuswahlForm, self).accept()