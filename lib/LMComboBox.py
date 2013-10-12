# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore

from CONSTANTS import *

class LMComboBox(QtGui.QComboBox):
	"""custom combobox for LagerManager"""
	
	def __init__(self, *args, **kwargs):
		"""
		* Sets up the subclassed QComboBox
		"""
		super(LMComboBox, self).__init__(*args, **kwargs)
		
		self._prevIndex = -1
		
		#self.connect(self, QtCore.SIGNAL('currentIndexChanged(int)'), self.onCurrentIndexChanged)
		
		
	def mousePressEvent(self, event):
		print "mousePressEvent"
		self._prevIndex = self.currentIndex()
		super(LMComboBox, self).mousePressEvent(event)
		
	def keyPressEvent(self, event):
		print "keyPressEvent"
		self._prevIndex = self.currentIndex()
		super(LMComboBox, self).keyPressEvent(event)
		
	def previousIndex(self):
		return self._prevIndex