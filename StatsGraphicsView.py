# -*- coding: utf8 -*-
"""A custom QGraphicsView that is zoomable by ctrl+mousewheel"""

from PyQt4 import QtCore, QtGui

from CONSTANTS import *
import GLOBALS

class StatsGraphicsView(QtGui.QGraphicsView):

	def __init__(self,*args, **kwargs):
		QtGui.QGraphicsView.__init__(self,*args, **kwargs)
		print "GVinit"
		
	def wheelEvent(self, event):
		numDegrees = event.delta() / 8;
		numSteps = numDegrees / 15;

		if GLOBALS.keyCtrlPressed:
			if (event.orientation() == QtCore.Qt.Vertical):
				if numDegrees > 0:
					self.scale(ZOOMINFACTOR, ZOOMINFACTOR)				
				else:
					self.scale(ZOOMOUTFACTOR, ZOOMOUTFACTOR)				
		
			event.accept()
		else:
			QtGui.QGraphicsView.wheelEvent(self, event)

