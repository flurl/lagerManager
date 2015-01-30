# -*- coding: utf-8 -*-
from PyQt4 import QtGui


class MultiColumnSortFilterProxyModel(QtGui.QSortFilterProxyModel):

	def filterAcceptsRow(self, source_row, source_parent):
		if self.filterKeyColumn() == -1:
			column_count = self.sourceModel().columnCount(source_parent)
			allDataStrings = u""
			for column in range(column_count):
				source_index = self.sourceModel().index(source_row, column, source_parent)
				allDataStrings += u" " + self.sourceModel().data(source_index, self.filterRole()).toString()
				allDataStrings = allDataStrings.toLower()
			
			return allDataStrings.contains(self.filterRegExp())
			return True

		else:
			return super(MultiColumnSortFilterProxyModel, self).filterAcceptsRow(source_row, source_parent)
		
		