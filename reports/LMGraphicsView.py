# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *

class LMGraphicsView(QtGui.QGraphicsView):
	
	def __init__(self, *args, **kwargs):
		"""
		* Sets up the subclassed QGraphicsView
		"""
		super(LMGraphicsView, self).__init__(*args, **kwargs)
		
		self.LastPanPoint = QtCore.QPoint()
		self.CurrentCenterPoint = QtCore.QPointF()
		self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)

		#Set-up the scene
		#Scene = new QGraphicsScene(self)
		#self.setScene(Scene)

		#Populate the scene
		"""for(int x = 0; x < 1000; x = x + 25) {
			for(int y = 0; y < 1000; y = y + 25) {

				if(x % 100 == 0 && y % 100 == 0) {
					Scene->addRect(x, y, 2, 2);

					QString pointString;
					QTextStream stream(&pointString);
					stream << "(" << x << "," << y << ")";
					QGraphicsTextItem* item = Scene->addText(pointString);
					item->setPos(x, y);
				} else {
					Scene->addRect(x, y, 1, 1);
				}
			}
		}

		//Set-up the view
		setSceneRect(0, 0, 1000, 1000);
		SetCenter(QPointF(500.0, 500.0)); //A modified version of centerOn(), handles special cases
		setCursor(Qt::OpenHandCursor);"""
		self.SetCenter(QtCore.QPointF(500.0, 500.0))
		
		self.connect(self.horizontalScrollBar(), QtCore.SIGNAL('sliderMoved(int)'), self.onScrollBarEvent)
	

	
	def SetCenter(self, centerPoint, onlyUpdate=False):
		"""
		* Sets the current centerpoint.  Also updates the scene's center point.
		* Unlike centerOn, which has no way of getting the floating point center
		* back, SetCenter() stores the center point.  It also handles the special
		* sidebar case.  This function will claim the centerPoint to sceneRec ie.
		* the centerPoint must be within the sceneRec.
		*"""
		#Get the rectangle of the visible area in scene coords
		visibleArea = self.mapToScene(self.rect()).boundingRect()

		#Get the scene area
		sceneBounds = self.sceneRect()

		boundX = visibleArea.width() / 2.0
		boundY = visibleArea.height() / 2.0
		boundWidth = sceneBounds.width() - 2.0 * boundX
		boundHeight = sceneBounds.height() - 2.0 * boundY

		#The max boundary that the centerPoint can be to
		bounds = QtCore.QRectF(boundX, boundY, boundWidth, boundHeight)

		if bounds.contains(centerPoint):
			#We are within the bounds
			self.CurrentCenterPoint = centerPoint
		else:
			#We need to clamp or use the center of the screen
			if visibleArea.contains(sceneBounds):
				#Use the center of scene ie. we can see the whole scene
				self.CurrentCenterPoint = sceneBounds.center()
			else:
				self.CurrentCenterPoint = centerPoint

				#We need to clamp the center. The centerPoint is too large
				if centerPoint.x() > (bounds.x() + bounds.width()):
					self.CurrentCenterPoint.setX(bounds.x() + bounds.width())
				elif centerPoint.x() < bounds.x():
					self.CurrentCenterPoint.setX(bounds.x())
				

				if centerPoint.y() > (bounds.y() + bounds.height()):
					self.CurrentCenterPoint.setY(bounds.y() + bounds.height())
				elif centerPoint.y() < bounds.y():
					self.CurrentCenterPoint.setY(bounds.y())

		if not onlyUpdate:
			#Update the scrollbars
			self.centerOn(self.CurrentCenterPoint)
		
		
	def GetCenter(self):
		return self.CurrentCenterPoint
	

	
	def mousePressEvent(self, event):
		"""
		* Handles when the mouse button is pressed
		"""
		#For panning the view
		self.LastPanPoint = event.pos()
		self.setCursor(QtCore.Qt.ClosedHandCursor)


	def mouseReleaseEvent(self, event):
		"""
		* Handles when the mouse button is released
		"""
		self.setCursor(QtCore.Qt.ArrowCursor)
		self.LastPanPoint = QtCore.QPoint()

	
	def mouseMoveEvent(self, event):
		"""
		*Handles the mouse move event
		"""
		pos = self.mapToScene(event.pos())
		object_ = self.scene().itemAt(pos)
		
		#if object_ is not None:
		#	object_.mouseMoveEvent(QtGui.QGraphicsSceneMouseEvent(event))
		
		if not self.LastPanPoint.isNull():
			#Get how much we panned
			delta = self.mapToScene(self.LastPanPoint) - self.mapToScene(event.pos())
			self.LastPanPoint = event.pos()
			
			#Update the center ie. do the pan
			self.SetCenter(self.GetCenter() + delta)
			
		else:
			QtGui.QGraphicsView.mouseMoveEvent(self, event)
			

	def wheelEvent(self, event):
		"""
		* Zoom the view in and out.
		"""
		if event.modifiers() & QtCore.Qt.ControlModifier == QtCore.Qt.ControlModifier:
			
			#Get the position of the mouse before scaling, in scene coords
			pointBeforeScale = QtCore.QPointF(self.mapToScene(event.pos()))

			#Get the original screen centerpoint
			screenCenter = self.GetCenter() #self.CurrentCenterPoint; //(visRect.center());

			#Scale the view ie. do the zoom
			if event.delta() > 0:
				#Zoom in
				self.scale(ZOOMINFACTOR, ZOOMINFACTOR)
			else:
				#Zooming out
				self.scale(ZOOMOUTFACTOR, ZOOMOUTFACTOR)

			#Get the position after scaling, in scene coords
			pointAfterScale = QtCore.QPointF(self.mapToScene(event.pos()))

			#Get the offset of how the screen moved
			offset = pointBeforeScale - pointAfterScale

			self.parent().plot()
			
			#Adjust to the new center for correct zooming
			newCenter = screenCenter + offset
			self.SetCenter(newCenter)
		else:
			QtGui.QGraphicsView.wheelEvent(self, event)
			
		self.updateCenterPointToVisibleArea()

	
	def resizeEvent(self, event):
		"""
		* Need to update the center so there is no jolt in the
		* interaction after resizing the widget.
		"""
		#Get the rectangle of the visible area in scene coords
		visibleArea = self.mapToScene(self.rect()).boundingRect()
		self.SetCenter(visibleArea.center())

		#Call the subclass resize so the scrollbars are updated correctly
		QtGui.QGraphicsView.resizeEvent(self, event)
		
		
	def onScrollBarEvent(self, value):
		self.updateCenterPointToVisibleArea()
	
	def updateCenterPointToVisibleArea(self):
		visibleArea = self.mapToScene(self.rect()).boundingRect()
		self.SetCenter(visibleArea.center(), True)
		
		
	def scale(self, *args, **kwargs):
		screenCenterBefore = self.GetCenter()
		super(LMGraphicsView, self).scale(*args, **kwargs)
		self.SetCenter(screenCenterBefore)
