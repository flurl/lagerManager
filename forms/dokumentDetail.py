# -*- coding: utf-8 -*-
#import datetime
import codecs

from PyQt4 import QtCore, QtGui, QtSql

from forms.formBase import FormBase
from ui.forms.dokumentDetailForm_gui import Ui_DokumentDetailForm

import config
from CONSTANTS import *


class DokumentDetailForm(FormBase):
	
	uiClass = Ui_DokumentDetailForm
	ident = 'dokumentDetail'
	
	def __init__(self, parent):
		FormBase.__init__(self, parent)
		self.docImage = None
		self.documentChanged = False
		
	def setupUi(self):
		super(DokumentDetailForm, self).setupUi()


	def setupSignals(self):
		#super(LieferungDetailForm, self).setupSignals()
		self.connect(self.ui.pushButton_fileChooser, QtCore.SIGNAL('clicked()'), self.chooseFile)
		self.connect(self.ui.label_documentImage, QtCore.SIGNAL('clicked()'), self.showImage)
		

	def setModel(self, model, idx):
		print 'setModel:', model, idx, idx.row()
		self.index = idx
		m = self.model = model
		#field index needs the name of the displayed field from the relational table
		relationModel = m.relationModel(m.fieldIndex('dot_bezeichnung')) 
		self.ui.comboBox_typ.setModel(relationModel)
		self.ui.comboBox_typ.setModelColumn(relationModel.fieldIndex('dot_bezeichnung'))
		
		mapper = QtGui.QDataWidgetMapper()
		mapper.setModel(m)
		mapper.setItemDelegate(QtSql.QSqlRelationalDelegate(m))
		mapper.addMapping(self.ui.lineEdit_id, m.fieldIndex('dok_id'))
		mapper.addMapping(self.ui.comboBox_typ, m.fieldIndex('dot_bezeichnung'))
		mapper.addMapping(self.ui.dateEdit_datum, m.fieldIndex('dok_datum'))
		mapper.addMapping(self.ui.lineEdit_bezeichnung, m.fieldIndex('dok_bezeichnung'))
		mapper.addMapping(self.ui.plainTextEdit_ocr, m.fieldIndex('dok_ocr'))
		mapper.setSubmitPolicy(QtGui.QDataWidgetMapper.ManualSubmit)
		mapper.setCurrentIndex(idx.row())
		self.mapper = mapper
		
		#for saving the record image blob
		self.connect(m, QtCore.SIGNAL('beforeUpdate (int,QSqlRecord&)'), self.onBeforeUpdate)
		self.connect(m, QtCore.SIGNAL('beforeInsert (QSqlRecord&)'), self.onBeforeInsert)
		
		self.ui.label_documentImage.setPixmap(self.scalePixmap(self.getCurrentDocImage()))
			
	def accept(self):
		self.mapper.submit()
		self.model.submitAll()
		super(DokumentDetailForm, self).accept()
		
	def reject(self):
		self.model.revertAll()
		super(DokumentDetailForm, self).reject()
		
		
	def getCurrentDocImage(self):
		ba = self.model.record(self.mapper.currentIndex()).value(self.model.fieldIndex('dok_data')).toByteArray()
		self.docImage = ba
		pic = QtGui.QPixmap()
		pic.loadFromData(ba)
		return pic
		
		
	def chooseFile(self):
		fileName = QtGui.QFileDialog.getOpenFileName(self, self.tr("Open Image"), "", self.tr("Image Files (*.png *.jpg *.bmp)"))
		print fileName
		image = QtGui.QImage(fileName)
		pic = QtGui.QPixmap.fromImage(image)
		self.ui.label_documentImage.setPixmap(self.scalePixmap(pic)) #Put image into QLabel object
		
		#load image to bytearray
		ba = QtCore.QByteArray()
		f = QtCore.QFile(fileName)
		if f.open(QtCore.QIODevice.ReadOnly):
			ba = f.readAll()
			f.close()
			self.docImage = ba
			self.documentChanged = True
		
		#if an .txt with the same name exists, use that as source for the text data
		try:
			fileName, ext = os.path.splitext(str(fileName))
			with codecs.open(fileName+'.txt', 'r', 'utf-8') as f:
				self.ui.plainTextEdit_ocr.setPlainText(f.read())
		except IOError as e:
			print 'No text file found'


	def scalePixmap(self, pm):
		return pm.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)

	def showImage(self):
		print 'clicked'
		if self.docImage is not None:
			print 'in if'
			label = QtGui.QLabel()
			pic = QtGui.QPixmap()
			pic.loadFromData(self.docImage)
			#Show the image into a QLabel object
			label.setPixmap(pic)
			
			area = QtGui.QScrollArea(self)
			area.setWidget(label)
			area.setWindowFlags(QtCore.Qt.Window)
			area.showMaximized()
		
	def onBeforeInsert(self, record):
		print 'onBeforeInsert'
		record.setValue('dok_data', self.docImage)

	def onBeforeUpdate(self, id_, record):
		print 'onBeforeUpdate'
		record.setValue('dok_data', self.docImage)
