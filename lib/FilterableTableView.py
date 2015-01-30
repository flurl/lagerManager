# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from ui.lib.FilterableTableView_gui import Ui_FilterableTableView
from lib.MultiColumnSortFilterProxyModel import MultiColumnSortFilterProxyModel


class FilterableTableView(QtGui.QWidget):
	
	def __getattr__(self, name):
		"""map all unknown attributes access to the tableview"""
		return getattr(self.tv, name)
	
	def __init__(self, *args, **kwargs):
		super(FilterableTableView, self).__init__(*args, **kwargs)
		
		self.ui = Ui_FilterableTableView()
		self.ui.setupUi(self)
		
		self.filterModel = MultiColumnSortFilterProxyModel()
		self.filterModel.setFilterKeyColumn(-1)
		self.filterModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
		
		
		self.tv = self.ui.tableView
		self.filterLayout = self.ui.layout_filters
		self.filterEdit = QtGui.QLineEdit()
		self.filterLayout.addWidget(self.filterEdit)
		self.connect(self.filterEdit, QtCore.SIGNAL('textEdited (const QString&)'), self.setFilter)
		
		
	def setModel(self, model):
		self.filterModel.setSourceModel(model)
		self.tv.setModel(self.filterModel)
		
	def setFilter(self, filterStr):
		filterStr = unicode(filterStr).strip()
		components = filterStr.split()
		
		andComponents = []
		orComponents = []
		filterRegExp = u""
		for component in components:
			if component[0] == u"+":
				andComponents.append(component[1:])
			else:
				orComponents.append(component)
			
		filterRegExp += u"("+u"|".join(orComponents)+")"
		for c in andComponents:
			filterRegExp += u"(?=.*%s)" % c
		
		self.filterModel.setFilterRegExp(filterRegExp)

