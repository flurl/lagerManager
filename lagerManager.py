#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymssql
import _mssql
import sqlite3
import decimal
import datetime
import time
import os
import sys
import random
import getopt

from PyQt4 import QtCore, QtGui

from ui.lagerManagerMainWindow_gui import Ui_MainWindow
#from articleSelectionDialog import ArticleSelectionDialog
from CONSTANTS import *
import DBConnection

import GLOBALS


class MainWindow(QtGui.QMainWindow):
	
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		
		#self.colors = {}   # colors for the articles
		#self.checkpoints = {}
		#self.activeArticles = None
		
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)	
	
		self._setupForm()
		
		self.openConnectDlg()
		
		self.statusBar().addPermanentWidget(QtGui.QLabel('Verbindung: '+DBConnection.connName))
		
	def _setupForm(self):
		self.connect(self.ui.actionQuit, QtCore.SIGNAL('triggered()'), self.close)
		
		self.connect(self.ui.action_Report_Lager_Lagerstand, QtCore.SIGNAL('triggered()'), self.openLagerstandReport)
		self.connect(self.ui.action_Report_Lager_MinimumLagerstand, QtCore.SIGNAL('triggered()'), self.openMinimumLagerstandReport)
		self.connect(self.ui.action_Report_Lager_Inventur, QtCore.SIGNAL('triggered()'), self.openInventurReport)
		self.connect(self.ui.action_Report_Verbrauch_Artikel, QtCore.SIGNAL('triggered()'), self.openArtikelVerbrauchReport)
		self.connect(self.ui.action_Report_Umsaetze_UmsatzAufwand, QtCore.SIGNAL('triggered()'), self.openUmsatzAufwandReport)
		self.connect(self.ui.action_Report_Einkauf_GesamteLieferungen, QtCore.SIGNAL('triggered()'), self.openGesamteLieferungenReport)
		
		self.connect(self.ui.action_Lieferungen_Lieferungen, QtCore.SIGNAL('triggered()'), self.openLieferungenForm)
		self.connect(self.ui.action_Lieferungen_Lieferanten, QtCore.SIGNAL('triggered()'), self.openLieferantenForm)
		self.connect(self.ui.action_Lieferungen_InitialerLagerstand, QtCore.SIGNAL('triggered()'), self.openInitialLagerstandForm)
		
		self.connect(self.ui.action_Stammdaten_Perioden, QtCore.SIGNAL('triggered()'), self.openPeriodenForm)
		self.connect(self.ui.action_Stammdaten_Import, QtCore.SIGNAL('triggered()'), self.openImportForm)

	def openConnectDlg(self):
		import connectDlg
		form = connectDlg.ConnectDialog(self)
		form.exec_()

	def openLagerstandReport(self):
		import reports.lagerstand
		report = reports.lagerstand.LagerstandReport()
		window = self.ui.mdiArea.addSubWindow(report)
		window.show()
		
	def openMinimumLagerstandReport(self):
		import reports.minimumLagerstand
		report = reports.minimumLagerstand.MinimumLagerstandReport()
		window = self.ui.mdiArea.addSubWindow(report)
		window.show()
		
	def openArtikelVerbrauchReport(self):
		import reports.verbrauch
		report = reports.verbrauch.VerbrauchReport()
		window = self.ui.mdiArea.addSubWindow(report)
		window.show()
		
	def openUmsatzAufwandReport(self):
		import reports.umsatzAufwand
		report = reports.umsatzAufwand.UmsatzAufwandReport()
		window = self.ui.mdiArea.addSubWindow(report)
		window.show()
		
	def openInventurReport(self):
		import reports.inventur
		report = reports.inventur.InventurReport()
		window = self.ui.mdiArea.addSubWindow(report)
		window.show()
	
	def openGesamteLieferungenReport(self):
		import reports.gesamteLieferungen
		report = reports.gesamteLieferungen.GesamteLieferungenReport()
		window = self.ui.mdiArea.addSubWindow(report)
		window.show()

		
	def openLieferungenForm(self):
		#import lieferungenDlg
		#form = lieferungenDlg.LieferungenDialog(self)
		#form.show()
		import forms.lieferung
		form = forms.lieferung.LieferungForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
		
	def openLieferantenForm(self):
		import forms.lieferanten
		form = forms.lieferanten.LieferantenForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
		
	def openInitialLagerstandForm(self):
		import lagerstandDlg
		form = lagerstandDlg.LagerstandDialog(self)
		form.show()
		
	def openPeriodenForm(self):
		import periodenDlg
		form = periodenDlg.PeriodenDialog(self)
		form.show()
		
	def openImportForm(self):
		import forms.dbImport
		form = forms.dbImport.ImportForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
		
		
	
						
				
				
if __name__ == "__main__":

	"""USER = 'wiffzack'
	PASSWORD = 'wiffzack'
	#DATABASE = 'wiffzack'
	SQLITEDB = 'WaWi.db'

	try:
	    opts, args = getopt.getopt(sys.argv[1:], "", ["host=", "database="])
	except getopt.GetoptError, err:
	    # print help information and exit:
	    print str(err) # will print something like "option -a not recognized"
	    sys.exit(2)

	for o, a in opts:
	    if o == '--host':
	        HOST = a
	    elif o == '--database':
			DATABASE = a
	    else:
	        assert False, "unhandled option"
	
	if os.name == 'nt': HOST = HOST+'/'+DATABASE
	else: HOST = HOST+':1433'
	
	if not HOST:
		print "No host specified"
		sys.exit(2)
	if not DATABASE:
		print "No database specified"
		sys.exit(2)"""

	
	app = QtGui.QApplication(sys.argv)
	app.setQuitOnLastWindowClosed(True)
	win = MainWindow()
	win.show()
	sys.exit(app.exec_())
