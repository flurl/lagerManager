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
from version import VERSION


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
		
		self.statusBar().addPermanentWidget(QtGui.QLabel('V'+unicode(VERSION)), 1)
		self.statusBar().addPermanentWidget(QtGui.QLabel('Verbindung: '+DBConnection.connName))
		
	def _setupForm(self):
		self.connect(self.ui.actionQuit, QtCore.SIGNAL('triggered()'), self.close)
		
		self.connect(self.ui.action_Report_Lager_Lagerstand, QtCore.SIGNAL('triggered()'), self.openLagerstandReport)
		self.connect(self.ui.action_Report_Lager_MinimumLagerstand, QtCore.SIGNAL('triggered()'), self.openMinimumLagerstandReport)
		self.connect(self.ui.action_Report_Lager_Inventur, QtCore.SIGNAL('triggered()'), self.openInventurReport)
		self.connect(self.ui.action_Report_Verbrauch_Artikel, QtCore.SIGNAL('triggered()'), self.openArtikelVerbrauchReport)
		self.connect(self.ui.action_Report_Umsaetze_UmsatzAufwand, QtCore.SIGNAL('triggered()'), self.openUmsatzAufwandReport)
		self.connect(self.ui.action_Report_Umsaetze_AufwanddetailsProTag, QtCore.SIGNAL('triggered()'), self.openAufwanddetailsProTagReport)
		self.connect(self.ui.action_Report_Umsaetze_DurchschUmsatzWochentag, QtCore.SIGNAL('triggered()'), self.openDurchschnittUmsatzProWochentagReport)
		self.connect(self.ui.action_Report_Einkauf_GesamteLieferungen, QtCore.SIGNAL('triggered()'), self.openGesamteLieferungenReport)
		self.connect(self.ui.action_Report_Einkauf_Verprobung, QtCore.SIGNAL('triggered()'), self.openVerprobungReport)
		self.connect(self.ui.action_Report_Personal_DienstnehmerStunden, QtCore.SIGNAL('triggered()'), self.openDienstnehmerStundenReport)
		
		self.connect(self.ui.action_Lieferungen_Lieferungen, QtCore.SIGNAL('triggered()'), self.openLieferungenForm)
		self.connect(self.ui.action_Lieferungen_Lieferanten, QtCore.SIGNAL('triggered()'), self.openLieferantenForm)
		self.connect(self.ui.action_Lieferungen_InitialerLagerstand, QtCore.SIGNAL('triggered()'), self.openInitialLagerstandForm)
		
		self.connect(self.ui.action_Dokumente_Dokumenttypen, QtCore.SIGNAL('triggered()'), self.openDokumenttypenForm)
		self.connect(self.ui.action_Dokumente_Dokumente, QtCore.SIGNAL('triggered()'), self.openDokumenteForm)		
		
		self.connect(self.ui.action_Personal_DienstplanErstellen, QtCore.SIGNAL('triggered()'), self.openDienstplanForm)
		self.connect(self.ui.action_Personal_Beschaeftigungsbereiche, QtCore.SIGNAL('triggered()'), self.openBeschaeftigungsbereicheForm)
		self.connect(self.ui.action_Personal_Arbeitsplaetze, QtCore.SIGNAL('triggered()'), self.openArbeitsplaetzeForm)
		self.connect(self.ui.action_Personal_Dienstnehmer, QtCore.SIGNAL('triggered()'), self.openDienstnehmerForm)
		self.connect(self.ui.action_Personal_DienstnehmerEreignisse, QtCore.SIGNAL('triggered()'), self.openDienstnehmerEreignisseForm)
		
		self.connect(self.ui.action_Stammdaten_Perioden, QtCore.SIGNAL('triggered()'), self.openPeriodenForm)
		self.connect(self.ui.action_Stammdaten_Import, QtCore.SIGNAL('triggered()'), self.openImportForm)
		self.connect(self.ui.action_Stammdaten_Steuersaetze, QtCore.SIGNAL('triggered()'), self.openSteuersaetzeForm)
		self.connect(self.ui.action_Stammdaten_Liefereinheiten, QtCore.SIGNAL('triggered()'), self.openLiefereinheitenForm)
		self.connect(self.ui.action_Stammdaten_Veranstaltungen, QtCore.SIGNAL('triggered()'), self.openVeranstaltungenForm)
		self.connect(self.ui.action_Stammdaten_Buchungskonten, QtCore.SIGNAL('triggered()'), self.openBuchungskontenForm)
		self.connect(self.ui.action_Stammdaten_DNEreignisTypen, QtCore.SIGNAL('triggered()'), self.openDNEreignisTypenForm)
		self.connect(self.ui.action_Stammdaten_Konfiguration, QtCore.SIGNAL('triggered()'), self.openConfigForm)
		

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
		
	def openAufwanddetailsProTagReport(self):
		import reports.aufwandDetailsProTag
		report = reports.aufwandDetailsProTag.AufwandDetailsProTagReport()
		window = self.ui.mdiArea.addSubWindow(report)
		window.show()
		
	def openDurchschnittUmsatzProWochentagReport(self):
		import reports.durchschnittUmsatzProTag
		report = reports.durchschnittUmsatzProTag.DurchschnittUmsatzProTagReport()
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
		
	def openVerprobungReport(self):
		import reports.verprobung
		report = reports.verprobung.VerprobungReport()
		window = self.ui.mdiArea.addSubWindow(report)
		window.show()
		
	def openDienstnehmerStundenReport(self):
		import reports.dienstnehmerStunden
		report = reports.dienstnehmerStunden.DienstnehmerStundenReport()
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
		import forms.lagerstand
		form = forms.lagerstand.LagerstandForm(self)
		form.show()
	
	def openDienstplanForm(self):
		import forms.dienstplan
		form = forms.dienstplan.DienstplanForm(self)
		form.show()
	
	def openBeschaeftigungsbereicheForm(self):
		import forms.beschaeftigungsbereiche
		form = forms.beschaeftigungsbereiche.BeschaeftigungsbereicheForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
		
	def openArbeitsplaetzeForm(self):
		import forms.arbeitsplaetze
		form = forms.arbeitsplaetze.ArbeitsplaetzeForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
	
	def openDienstnehmerForm(self):
		import forms.dienstnehmer
		form = forms.dienstnehmer.DienstnehmerForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
		
	def openDienstnehmerEreignisseForm(self):
		import forms.dienstnehmerEreignisse
		form = forms.dienstnehmerEreignisse.DienstnehmerEreignisseForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
		
	def openPeriodenForm(self):
		import periodenDlg
		form = periodenDlg.PeriodenDialog(self)
		form.show()
		
	def openImportForm(self):
		import forms.dbImport
		form = forms.dbImport.ImportForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
		
	def openDokumenteForm(self):
		import forms.dokumente
		form = forms.dokumente.DokumenteForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
		
	def openDokumenttypenForm(self):
		import forms.dokumenttypen
		form = forms.dokumenttypen.DokumenttypenForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
		
	def openSteuersaetzeForm(self):
		import forms.steuersaetze
		form = forms.steuersaetze.SteuersaetzeForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
		
	def openLiefereinheitenForm(self):
		import forms.liefereinheiten
		form = forms.liefereinheiten.LiefereinheitenForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
		
	def openVeranstaltungenForm(self):
		import forms.veranstaltungen
		form = forms.veranstaltungen.VeranstaltungenForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
		
	def openBuchungskontenForm(self):
		import forms.buchungskonten
		form = forms.buchungskonten.BuchungskontenForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
		
	def openDNEreignisTypenForm(self):
		import forms.dirTypen
		form = forms.dirTypen.DirTypenForm(self)
		window = self.ui.mdiArea.addSubWindow(form)
		window.show()
				
	def openConfigForm(self):
		import forms.globalConfig
		form = forms.globalConfig.ConfigForm(self)
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
