# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from ui.lib.FilterableTableView_gui import Ui_FilterableTableView


class FilterableTableView(QtGui.QWidget):
	
	def __getattr__(self, name):
		"""map all unknown attributes access to the tableview"""
		return getattr(self.tv, name)
	
	def __init__(self, *args, **kwargs):
		super(FilterableTableView, self).__init__(*args, **kwargs)
		
		self.ui = Ui_FilterableTableView()
		self.ui.setupUi(self)
		
		self.filterModel = QtGui.QSortFilterProxyModel()
		self.filterModel.setFilterKeyColumn(-1)
		self.filterModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
		
		
		self.tv = self.ui.tableView
		self.filterLayout = self.ui.layout_filters
		self.filterEdit = QtGui.QLineEdit()
		self.filterLayout.addWidget(self.filterEdit)
		self.connect(self.filterEdit, QtCore.SIGNAL('textEdited (const QString&)'), self.filterModel.setFilterFixedString)
		
		
	def setModel(self, model):
		self.filterModel.setSourceModel(model)
		self.tv.setModel(self.filterModel)
