# -*- coding: utf8 -*-
import pymssql
import sys

from PyQt4 import QtCore, QtGui

from ui.articleSelectionDialog_gui import Ui_ArticleSelectionDialog

class ArticleSelectionDialog(QtGui.QDialog):
	
	def __init__(self, parent):
		
		QtGui.QDialog.__init__(self, parent)
		
		self._parent = parent
		
		self.ui = Ui_ArticleSelectionDialog()

		self.ui.setupUi(self)		
		
		self._setupForm()

	
	
	def _setupForm(self):
		
		self._populateTable()
		self.connect(self.ui.pushButton_ok, QtCore.SIGNAL('clicked()'), self._onOKBtnPressed)
		self.connect(self.ui.pushButton_set, QtCore.SIGNAL('clicked()'), self._onSetBtnPressed)
		self.connect(self.ui.pushButton_checkAll, QtCore.SIGNAL('clicked()'), self._onCheckAllBtnPressed)
		self.connect(self.ui.pushButton_uncheckAll, QtCore.SIGNAL('clicked()'), self._onUncheckAllBtnPressed)
		
		
		
	def _onOKBtnPressed(self):
		self._setActiveArticles()
		self._saveConfig()
		self.accept()
		
		
		
	def _onSetBtnPressed(self):
		self._setActiveArticles()



	def _onCheckAllBtnPressed(self):
		checkState = QtCore.Qt.Checked
		for i in range(0, self.ui.tableWidget_articles.rowCount()):
			self.ui.tableWidget_articles.item(i, 1).setCheckState(checkState)
		
		
		
	def _onUncheckAllBtnPressed(self):
		checkState = QtCore.Qt.Unchecked
		for i in range(0, self.ui.tableWidget_articles.rowCount()):
			self.ui.tableWidget_articles.item(i, 1).setCheckState(checkState)
			
	
	
	def _populateTable(self):
		
		self.ui.tableWidget_articles.setRowCount(0)
		self.ui.tableWidget_articles.setColumnCount(2)
		self.ui.tableWidget_articles.hideColumn(0)
		
		articles = self._parent.checkpoints[self._parent.checkpoints.keys()[0]]['articles']
		keys = sorted(articles.keys())
		for name in keys:
			values = articles[name]
			newRow = self.ui.tableWidget_articles.rowCount()
			self.ui.tableWidget_articles.insertRow(newRow)
			
			tabWidget = QtGui.QTableWidgetItem(name)
			self.ui.tableWidget_articles.setItem(newRow, 0, tabWidget)
			
			tabWidget = QtGui.QTableWidgetItem(unicode(name, 'iso8859-1'))
			tabWidget.setFlags(QtCore.Qt.ItemFlag(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled))
			if self._parent.activeArticles is None or name in self._parent.activeArticles: checkState = QtCore.Qt.Checked
			else: checkState = QtCore.Qt.Unchecked
			tabWidget.setCheckState(checkState)
			
			self.ui.tableWidget_articles.setItem(newRow, 1, tabWidget)
		
	
	def _setActiveArticles(self):
		vals = []
		for i in range(0, self.ui.tableWidget_articles.rowCount()):
			if self.ui.tableWidget_articles.item(i, 1).checkState() == QtCore.Qt.Checked: 
				vals.append(self.ui.tableWidget_articles.item(i, 0).text())
				
		self._parent.activeArticles = vals
		self._parent.plot()
	
	
	def _saveConfig(self):
		pass
	
		
		
	
	