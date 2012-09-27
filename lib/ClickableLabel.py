# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui


class ClickableLabel(QtGui.QLabel):

	def __init(self, parent):
		QtGui.QLabel.__init__(self, parent)

	def mouseReleaseEvent(self, ev):
		self.emit(QtCore.SIGNAL('clicked()'))

