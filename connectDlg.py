# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from ui.connectDlg_gui import Ui_ConnectDialog

from CONSTANTS import *
import config
import DBConnection

class ConnectDialog(QtGui.QDialog):
	
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)

		self.ui = Ui_ConnectDialog()
		self.ui.setupUi(self)
		
		self.connect(self.ui.pushButton_connect, QtCore.SIGNAL('clicked()'), self.connectToDb)
		
		#try:
		#	c = config.config['app_db_connections']['all']
		#	for params in c:
		#		print params['host']
		#		self.ui.comboBox_host.addItem(params['host'])
		#		self.ui.comboBox_db.addItem(params['db'])
		#		self.ui.comboBox_user.addItem(params['user'])
		#except KeyError:
		#	pass
			
			
		try:
			c = config.config['app_db_connections']['last']
			self.ui.comboBox_host.addItem(c['host'])
			self.ui.comboBox_db.addItem(c['db'])
			self.ui.comboBox_user.addItem(c['user'])
		except KeyError:
			pass
		
#		self._connectToDb()
#		self._setupForm()


	def connectToDb(self):
		host = unicode(self.ui.comboBox_host.currentText())
		db = unicode(self.ui.comboBox_db.currentText())
		user = unicode(self.ui.comboBox_user.currentText())
		pw = unicode(self.ui.lineEdit_pw.text())
		
		if DBConnection.connect(host, user, pw, db):
			connParams = {'host': host, 'db': db, 'user': user}
			try:
				c = config.config['app_db_connections']
			except KeyError:
				config.config['app_db_connections'] = {}
			
#			try:
#				allConnections = config.config['app_db_connections']['all']
#			except KeyError:
#				allConnections = config.config['app_db_connections']['all'] = {}
				
#			if connParams not in allConnections:
#				allConnections.append(connParams)
				
			config.config['app_db_connections']['last'] = connParams
			config.config.write()
			self.accept()
		else:
			QtGui.QMessageBox.critical(self, 'Verbindung fehlgeschlagen', 'Verbindung fehlgeschlagen', QtGui.QMessageBox.Ok)
		
		

