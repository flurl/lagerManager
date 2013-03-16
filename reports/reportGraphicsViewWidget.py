import random
import math
import copy

from PyQt4 import QtCore, QtGui

from CONSTANTS import *

from ui.reports.reportGraphicsView_gui import Ui_ReportGraphicsView

LEGENDWIDTH = 300
INFOPOPUPWIDTH = 200
INFOPOPUPHEIGHT = 50
INFOPOPUPLINEHEIGHT = 20
INFOPOPUPSPACING = 15

class Rect(QtGui.QGraphicsRectItem):
	Type = QtGui.QGraphicsRectItem.UserType + 1

	def __init__(self, formatter, *args):
		QtGui.QGraphicsRectItem.__init__(self, *args)
		
		self._showInfo = False
		self.data = []
		self.extraData = []
		self.dataFormatter = formatter
		self.dataLines = 1
		self.seriesId = None

	def type(self):
		return Rect.Type

	def setData(self, data):
		self.data = data
		
	def setExtraData(self, data):
		self.extraData = data
		
	def setSeriesId(self, id_):
		self.seriesId = id_

	def paint(self, painter, option, widget):
		QtGui.QGraphicsRectItem.paint(self, painter, option, widget)

		if self._showInfo:			
			currScaling = self.getCurrentScaling()
		
			f = QtGui.QFont("sans-serif", 10*currScaling[0], QtGui.QFont.Normal);
			painter.setFont(f)

			x, y = self.rect().x(), self.rect().y()
			painter.setPen(QtGui.QPen(QtGui.QColor(0,0,0)))
			painter.setBrush(QtCore.Qt.gray)
			lines = 0
			for i in range(len(self.data)):
				y += INFOPOPUPLINEHEIGHT*currScaling[1]
				text = unicode(self.data[i])
				if self.dataFormatter and callable(self.dataFormatter[i]):
					text = self.dataFormatter[i](text)
				painter.setPen(QtGui.QPen(QtCore.Qt.gray))
				painter.drawRect(x+INFOPOPUPSPACING, y-INFOPOPUPLINEHEIGHT*currScaling[1], INFOPOPUPWIDTH*currScaling[0], (INFOPOPUPLINEHEIGHT+INFOPOPUPSPACING)*currScaling[1])
				painter.setPen(QtGui.QPen(QtGui.QColor(0,0,0)))
				painter.drawText(x+20, y, text)
				lines += 1
			for i in range(len(self.extraData)):
				y += INFOPOPUPLINEHEIGHT*currScaling[1]
				text = unicode(self.extraData[i])
				painter.setPen(QtGui.QPen(QtCore.Qt.gray))
				painter.drawRect(x+INFOPOPUPSPACING, y-INFOPOPUPLINEHEIGHT*currScaling[1], INFOPOPUPWIDTH*currScaling[0], (INFOPOPUPLINEHEIGHT+INFOPOPUPSPACING)*currScaling[1])
				painter.setPen(QtGui.QPen(QtGui.QColor(0,0,0)))
				painter.drawText(x+20, y, text)
				lines += 1
			self.dataLines = lines
			
			
			
			#gradient = QtGui.QRadialGradient(-3, -3, 10)
			#if option.state & QtGui.QStyle.State_Sunken:
				#gradient.setCenter(3, 3)
				#gradient.setFocalPoint(3, 3)
				#gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.yellow).light(120))
				#gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkYellow).light(120))
			#else:
				#gradient.setColorAt(0, QtCore.Qt.yellow)
				#gradient.setColorAt(1, QtCore.Qt.darkYellow)
	
			#painter.setBrush(QtGui.QBrush(gradient))
			#painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
			#painter.drawEllipse(-10, -10, 20, 20)

	def hoverEnterEvent(self, event):
		self._showInfo = True
		self.setZValue(1000)
		self.update()

	def hoverLeaveEvent(self, event):
		self._showInfo = False
		self.setZValue(0)
		self.update()
		
	def getCurrentScaling(self):
		try:
			gvMatrix = self.scene().views()[0].matrix()
			currScaling = (1/gvMatrix.m11(), 1/gvMatrix.m22())
		except IndexError:
			currScaling = (1.0, 1.0)
		return currScaling
	
	def boundingRect(self):
		currScaling = self.getCurrentScaling()
		
		lines = self.dataLines
		if lines < 5: lines = 5
		rect = QtGui.QGraphicsRectItem.boundingRect(self)
		return QtCore.QRectF(rect.x(), rect.y(), rect.width()+INFOPOPUPWIDTH*currScaling[0]+INFOPOPUPSPACING*2, rect.height()+INFOPOPUPLINEHEIGHT+INFOPOPUPSPACING*2*lines*currScaling[1])
	
	def contextMenuEvent(self, event):
		menu = QtGui.QMenu()
		showOnlyAction = menu.addAction('Nur diese Datenreihe anzeigen')
		showAllAction = menu.addAction('Alle Datenreihen anzeigen')
		action = menu.exec_(QtCore.QPoint(event.screenPos()))
		gvw = self.scene().views()[0].parent()
		if action == showOnlyAction:
			gvw.onlyShowSeries(self.seriesId)
		elif action == showAllAction:
			gvw.showAllSeries()
			



class ReportGraphicsViewWidget(QtGui.QWidget):
	
	def __init__(self, parent):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_ReportGraphicsView()
		self.ui.setupUi(self)
		
		self.dataPoints = []
		self.extraData = []
		self.dataFormatter = []
		self.markingData = []
		self.maxXCoord = 0
		self.dpFilter = []
		
		self.connect(self.ui.slider_minDP, QtCore.SIGNAL('valueChanged (int)'), self._onMinDpSliderChanged)
		self.connect(self.ui.slider_maxDP, QtCore.SIGNAL('valueChanged (int)'), self._onMaxDpSliderChanged)
		
		self.connect(self.ui.pushButton_zoomIn, QtCore.SIGNAL('clicked()'), self.zoomIn)
		self.connect(self.ui.pushButton_zoomOut, QtCore.SIGNAL('clicked()'), self.zoomOut)
		
		self.connect(self.ui.checkBox_highlightNegative, QtCore.SIGNAL('stateChanged (int)'), self.onHighlightNegativeChanged)
		
		self.connect(self.ui.checkBox_showMarkings, QtCore.SIGNAL('stateChanged(int)'), self.onShowMarkingsChanged)
		
		self.connect(self.ui.checkBox_filterActivated, QtCore.SIGNAL('stateChanged(int)'), self.onFilterActivatedChanged)
	
	def setDatapoints(self, dp = None):
		#print 'ReportWidget:setDatapoints', dp
		if dp is None:
			dp = {}
		self.dataPoints = dp
		
		self.ui.slider_minDP.setMaximum(len(dp))
		self.ui.slider_maxDP.setMaximum(len(dp))
		self.ui.spinBox_minDP.setMaximum(len(dp))
		self.ui.spinBox_maxDP.setMaximum(len(dp))
		self.ui.slider_maxDP.setValue(len(dp))
			
			
	def plot(self):
		gv = self.ui.graphicsView
		
		scene = QtGui.QGraphicsScene(gv)
		scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
		
		maxY = 0
		
		dp = self.filterDp()
		
		#for x in dp:
		for x in range(len(dp)):
			for y in dp[x]:
				if maxY < dp[x][y]:
					maxY = dp[x][y]
		if maxY != 0:
			yScalingFactor = 10**(4/maxY) #this makes reports with small y values more readable
		else:
			yScalingFactor = 1

		oldCoords = {}
		colors = {}
		min_ = self.ui.slider_minDP.value()
		max_ = self.ui.slider_maxDP.value()
		currScaling = self.getCurrentScaling()
		highlightNegative = self.ui.checkBox_highlightNegative.isChecked()
		self.maxXCoord = 0
		for x in range(len(dp)):
			if x >= min_ and x <= max_:
				for y in dp[x]:
					if y not in colors.keys():
						colors[y] = QtGui.QColor(random.randint(0,255),	random.randint(0,255),random.randint(0,255))
					color = colors[y]
					pen = QtGui.QPen(color)
					coords = (LEGENDWIDTH+x*200, (maxY - dp[x][y])*yScalingFactor)
					if self.maxXCoord < coords[0]:
						self.maxXCoord = coords[0]
				
					#print y, x, dp[x][y]
					rect = Rect(self.dataFormatter, QtCore.QRectF(coords[0], coords[1], 5*currScaling[0], 5*currScaling[1]))
		
					rect.setPen(pen)
					rect.setBrush(color)
					rect.setAcceptHoverEvents(True)
					#rect.setZValue(100)
					rect.setSeriesId(y)
					rect.setData([y, x, dp[x][y]])
					try:
						rect.setExtraData(self.extraData[x][y])
					except IndexError:
						pass
				
					scene.addItem(rect)

					if highlightNegative and dp[x][y]<0:
						triangle = QtGui.QGraphicsPolygonItem(QtGui.QPolygonF([QtCore.QPointF(coords[0], coords[1]+10*currScaling[1]),
													QtCore.QPointF(coords[0]+5*currScaling[0], coords[1]+(10+10)*currScaling[1]),
													QtCore.QPointF(coords[0]-5*currScaling[0], coords[1]+(10+10)*currScaling[1]),
													QtCore.QPointF(coords[0], coords[1]+10*currScaling[1])]))
						triangle.setPen(pen)
						scene.addItem(triangle)
				
				
					if y in oldCoords:
						scene.addLine(oldCoords[y][0], oldCoords[y][1], coords[0]+5, coords[1]+5, pen)
					oldCoords[y] = (coords[0]+5, coords[1]+5)
		
		width = scene.width()+50
		
		scene.addLine(LEGENDWIDTH, maxY*yScalingFactor, width, maxY*yScalingFactor)  #x-axis
		scene.addLine(LEGENDWIDTH, 0, LEGENDWIDTH, maxY*yScalingFactor) #y-axis
		
		#horizontal guides
		"""pen = QtGui.QPen(QtGui.QColor(200, 200, 200))
		for i in range(0, int(max), 100):
			scene.addLine(LEGENDWIDTH-10, max-i, width, max-i, pen)
			text = scene.addText(str(i))
			text.setPos(LEGENDWIDTH-50, max-i)"""
		
		gv.setScene(scene)
		gv.setCacheMode(QtGui.QGraphicsView.CacheBackground)
		gv.setRenderHint(QtGui.QPainter.Antialiasing)
		#gv.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
		#gv.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
		
		self.updateMarking()
	
	
	def getCurrentScaling(self):
		try:
			gvMatrix = self.ui.graphicsView.scene().views()[0].matrix()
			currScaling = (1/gvMatrix.m11(), 1/gvMatrix.m22())
		except (IndexError, AttributeError):
			currScaling = (1.0, 1.0)
		return currScaling
	
	
	def setDataFormatter(self, f):
		self.dataFormatter = f
	
	def setExtraData(self, data):
		self.extraData = data
		
	def setMarkingData(self, markingData):
		self.markingData = markingData

	def zoomIn(self):
		self.ui.graphicsView.scale(ZOOMINFACTOR, ZOOMINFACTOR)
		self.plot()
		
	def zoomOut(self):
		self.ui.graphicsView.scale(ZOOMOUTFACTOR, ZOOMOUTFACTOR)
		self.plot()
		
	def _onMinDpSliderChanged(self, newVal):
		max_ = self.ui.slider_maxDP.value()
		if max_ < newVal:
			self.ui.slider_maxDP.setValue(newVal)
		self.plot()

	def _onMaxDpSliderChanged(self, newVal):
		min_ = self.ui.slider_minDP.value()
		if min_ > newVal:
			self.ui.slider_minDP.setValue(newVal)
		self.plot()
		
	def onHighlightNegativeChanged(self, state):
		self.plot()
		
	def onShowMarkingsChanged(self, state):
		self.plot()
		
	def updateMarking(self):
		if self.ui.checkBox_showMarkings.isChecked():
			scene = self.ui.graphicsView.scene()
			
			currScaling = self.getCurrentScaling()
			textGapFactor = math.floor(currScaling[0]/12)+1
			coords = (0,scene.height())
			
			#width = scene.width()
			width = self.maxXCoord
			
			#rect = QtGui.QGraphicsRectItem(QtCore.QRectF(coords[0]+LEGENDWIDTH, coords[1], width-(LEGENDWIDTH), 50*currScaling[1]))
			
			color = QtGui.QColor(0xdd,	0xdd, 0xdd)
			pen = QtGui.QPen(color)
			#scene.addItem(rect)
			
			for x in range(len(self.dataPoints)):
				if x%textGapFactor == 0:
					dpCoords = (LEGENDWIDTH+x*200,coords[1])
					scene.addLine(dpCoords[0], dpCoords[1]-150*currScaling[1], dpCoords[0], dpCoords[1]-100*currScaling[1], pen)
					textItem = QtGui.QGraphicsTextItem()
					textItem.setPos(dpCoords[0]-15*currScaling[0],dpCoords[1])
					
					try:
						text = self.markingData[x]
					except IndexError:
						text = x
					
					textItem.setPlainText(unicode(text))
					textItem.rotate(270)
					textItem.setScale(currScaling[0])

					scene.addItem(textItem)
				
	def onlyShowSeries(self, seriesId):
		self.dpFilter.append(seriesId)
		cb = self.ui.checkBox_filterActivated
		cb.setChecked(QtCore.Qt.Checked)
		cb.setEnabled(True)
		self.plot()
		
	def showAllSeries(self):
		self.dpFilter = []
		cb = self.ui.checkBox_filterActivated
		cb.setChecked(QtCore.Qt.Unchecked)
		cb.setEnabled(False)
		self.plot()
		
	def filterDp(self):
		if len(self.dpFilter) > 0:
			dp = []
			for f in self.dpFilter:
				for x in range(len(self.dataPoints)):
					dp.append({})
					for y in self.dataPoints[x]:
						if y in f:
							dp[x][y] = self.dataPoints[x][y]
			return dp
		else:
			return copy.deepcopy(self.dataPoints)
		
	def onFilterActivatedChanged(self, state):
		if len(self.dpFilter) > 0 and state == QtCore.Qt.Unchecked:
			self.showAllSeries()