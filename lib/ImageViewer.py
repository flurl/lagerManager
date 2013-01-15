# -*- coding: utf-8 -*-

#############################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

from PyQt4 import QtCore, QtGui
import lagerManager_rc


class ImageViewer(QtGui.QMainWindow):
	def __init__(self, parent):
		super(ImageViewer, self).__init__(parent)
		
		self.printer = QtGui.QPrinter()
		self.scaleFactor = 0.0

		self.imageLabel = QtGui.QLabel()
		self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
		self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
				QtGui.QSizePolicy.Ignored)
		self.imageLabel.setScaledContents(True)

		self.scrollArea = QtGui.QScrollArea()
		self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
		self.scrollArea.setWidget(self.imageLabel)
		self.setCentralWidget(self.scrollArea)

		self.createActions()
		self.createMenus()
		self.createToolbar()

		self.setWindowTitle("Image Viewer")
		self.resize(500, 400)

	def open(self):
		fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
				QtCore.QDir.currentPath())
		if fileName:
			image = QtGui.QImage(fileName)
			if image.isNull():
				QtGui.QMessageBox.information(self, "Image Viewer",
				        "Cannot load %s." % fileName)
				return

			self.setPixmap(QtGui.QPixmap.fromImage(image))

	def setPixmap(self, pixmap):
		self.imageLabel.setPixmap(pixmap)
		self.scaleFactor = 1.0

		self.printAct.setEnabled(True)
		self.fitToWindowAct.setEnabled(True)
		self.updateActions()

		if not self.fitToWindowAct.isChecked():
			self.imageLabel.adjustSize()
		
		
	def print_(self):
		dialog = QtGui.QPrintDialog(self.printer, self)
		if dialog.exec_():
			painter = QtGui.QPainter(self.printer)
			rect = painter.viewport()
			size = self.imageLabel.pixmap().size()
			size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
			painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
			painter.setWindow(self.imageLabel.pixmap().rect())
			painter.drawPixmap(0, 0, self.imageLabel.pixmap())

	def zoomIn(self):
		self.scaleImage(1.25)

	def zoomOut(self):
		self.scaleImage(0.8)

	def normalSize(self):
		self.imageLabel.adjustSize()
		self.scaleFactor = 1.0

	def fitToWindow(self):
		fitToWindow = self.fitToWindowAct.isChecked()
		self.scrollArea.setWidgetResizable(fitToWindow)
		if not fitToWindow:
			self.normalSize()

		self.updateActions()
		
	def rotateCw(self):
		self.rotate(90)
		
	def rotateCcw(self):
		self.rotate(-90)
		
	def rotate(self, degrees):
		pm = self.imageLabel.pixmap()
		mat = QtGui.QMatrix()
		mat.rotate(degrees)  #rotation operation
		pm1 = pm.transformed(mat)  #saving the changed QPixmap in a new QPixmap
		self.imageLabel.setPixmap(pm1)  #setting changed Pixmap on the label
		self.adjustLabelSize()


	def about(self):
		QtGui.QMessageBox.about(self, "About Image Viewer",
				"<p>The <b>Image Viewer</b> example shows how to combine "
				"QLabel and QScrollArea to display an image. QLabel is "
				"typically used for displaying text, but it can also display "
				"an image. QScrollArea provides a scrolling view around "
				"another widget. If the child widget exceeds the size of the "
				"frame, QScrollArea automatically provides scroll bars.</p>"
				"<p>The example demonstrates how QLabel's ability to scale "
				"its contents (QLabel.scaledContents), and QScrollArea's "
				"ability to automatically resize its contents "
				"(QScrollArea.widgetResizable), can be used to implement "
				"zooming and scaling features.</p>"
				"<p>In addition the example shows how to use QPainter to "
				"print an image.</p>")

	def createActions(self):
		self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
				triggered=self.open)

		self.printAct = QtGui.QAction("&Print...", self, shortcut="Ctrl+P",
				enabled=False, triggered=self.print_)

		self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
				triggered=self.close)

		self.zoomInAct = QtGui.QAction(QtGui.QIcon(':/images/zoom-in.svg'), "Zoom &In (25%)", self,
				shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)

		self.zoomOutAct = QtGui.QAction(QtGui.QIcon(':/images/zoom-out.svg'), "Zoom &Out (25%)", self,
				shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)

		self.normalSizeAct = QtGui.QAction(QtGui.QIcon(':/images/zoom-original.svg'), "&Normal Size", self,
				shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)

		self.fitToWindowAct = QtGui.QAction(QtGui.QIcon(':/images/zoom-best-fit.svg'), "&Fit to Window", self,
				enabled=False, checkable=True, shortcut="Ctrl+F",
				triggered=self.fitToWindow)
				
		self.rotateCwAct = QtGui.QAction(QtGui.QIcon(':/images/rotate-right.svg'), u'90° &im Uhrzeigersinn', self,
				shortcut='Ctrl+i', enabled=True, triggered=self.rotateCw)
				
		self.rotateCcwAct = QtGui.QAction(QtGui.QIcon(':/images/rotate-left.svg'), u'90° &gegen Uhrzeigersinn', self,
				shortcut='Ctrl+g', enabled=True, triggered=self.rotateCcw)

		self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)

		self.aboutQtAct = QtGui.QAction("About &Qt", self,
				triggered=QtGui.qApp.aboutQt)

	def createMenus(self):
		self.fileMenu = QtGui.QMenu("&File", self)
		self.fileMenu.addAction(self.openAct)
		self.fileMenu.addAction(self.printAct)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.exitAct)

		self.viewMenu = QtGui.QMenu("&View", self)
		self.viewMenu.addAction(self.zoomInAct)
		self.viewMenu.addAction(self.zoomOutAct)
		self.viewMenu.addAction(self.normalSizeAct)
		self.viewMenu.addSeparator()
		self.viewMenu.addAction(self.fitToWindowAct)
		self.viewMenu.addSeparator()
		self.viewMenu.addAction(self.rotateCwAct)
		self.viewMenu.addAction(self.rotateCcwAct)

		self.helpMenu = QtGui.QMenu("&Help", self)
		self.helpMenu.addAction(self.aboutAct)
		self.helpMenu.addAction(self.aboutQtAct)

		self.menuBar().addMenu(self.fileMenu)
		self.menuBar().addMenu(self.viewMenu)
		self.menuBar().addMenu(self.helpMenu)
		
	def createToolbar(self):
		tb = self.toolbar = self.addToolBar(u'View')
		tb.addAction(self.zoomInAct)
		tb.addAction(self.zoomOutAct)
		tb.addAction(self.normalSizeAct)
		tb.addSeparator()
		tb.addAction(self.fitToWindowAct)
		tb.addSeparator()
		tb.addAction(self.rotateCwAct)
		tb.addAction(self.rotateCcwAct)

	def updateActions(self):
		self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
		self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
		self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

	def scaleImage(self, factor):
		self.scaleFactor *= factor
		self.adjustLabelSize()

		self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
		self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

		self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
		self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

	def adjustScrollBar(self, scrollBar, factor):
		scrollBar.setValue(int(factor * scrollBar.value()
				                + ((factor - 1) * scrollBar.pageStep()/2)))
				                
	def adjustLabelSize(self):
		self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())


if __name__ == '__main__':

	import sys

	app = QtGui.QApplication(sys.argv)
	imageViewer = ImageViewer()
	imageViewer.show()
	sys.exit(app.exec_())