# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

class ColorDialogDelegate(QtSql.QSqlRelationalDelegate):
	"""this class shows a push button to open a QColorDialog"""
	
	def __init__(self, *args, **kwargs):
		super(ColorDialogDelegate, self).__init__(*args, **kwargs)
		self.colorColumn = -1
		self.prevData = None

	def createEditor(self, parent, option, index):
		if index.column() == self.colorColumn:
				button = QtGui.QPushButton(parent)
				self.connect(button, QtCore.SIGNAL('clicked()'), lambda i=index: self.openColorDialog(index))
				return button
		return super(ColorDialogDelegate, self).createEditor(parent, option, index)
	
	
	def paint(self, painter, option, index):
		opt = QtGui.QStyleOptionViewItem(option)
		if index.column() == self.colorColumn:
			color = QtGui.QColor(index.data().toString())
			painter.fillRect(option.rect, color)
		return super(ColorDialogDelegate, self).paint(painter, opt, index)
	
	
	def editorEvent (self, event, model, option, index):
		if index.column() == self.colorColumn:
			self.prevData = index.data()
		return super(ColorDialogDelegate, self).editorEvent(event, model, option, index)
	
	
	def setColorColumn(self, col):
		self.colorColumn = col
		
		
	def openColorDialog(self, idx):
		color = QtGui.QColorDialog.getColor()
		if color.isValid():
			idx.model().setData(idx, color.name())
		else:
			color = QtGui.QColor(self.prevData)
			if color.isValid():
				idx.model().setData(idx, color.name())
		


