# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/lagerManagerMainWindow.ui'
#
# Created: Tue Jun 25 20:50:21 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1047, 664)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.mdiArea = QtGui.QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName(_fromUtf8("mdiArea"))
        self.horizontalLayout.addWidget(self.mdiArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1047, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menu_Reports = QtGui.QMenu(self.menubar)
        self.menu_Reports.setObjectName(_fromUtf8("menu_Reports"))
        self.menu_Einkauf = QtGui.QMenu(self.menu_Reports)
        self.menu_Einkauf.setObjectName(_fromUtf8("menu_Einkauf"))
        self.menu_Umsaetze = QtGui.QMenu(self.menu_Reports)
        self.menu_Umsaetze.setObjectName(_fromUtf8("menu_Umsaetze"))
        self.menu_Verbrauch = QtGui.QMenu(self.menu_Reports)
        self.menu_Verbrauch.setObjectName(_fromUtf8("menu_Verbrauch"))
        self.menu_Lagerstand = QtGui.QMenu(self.menu_Reports)
        self.menu_Lagerstand.setObjectName(_fromUtf8("menu_Lagerstand"))
        self.menu_Personal_2 = QtGui.QMenu(self.menu_Reports)
        self.menu_Personal_2.setObjectName(_fromUtf8("menu_Personal_2"))
        self.menu_Lieferungen = QtGui.QMenu(self.menubar)
        self.menu_Lieferungen.setObjectName(_fromUtf8("menu_Lieferungen"))
        self.menuStammdaten = QtGui.QMenu(self.menubar)
        self.menuStammdaten.setObjectName(_fromUtf8("menuStammdaten"))
        self.menu_Dokumente = QtGui.QMenu(self.menubar)
        self.menu_Dokumente.setObjectName(_fromUtf8("menu_Dokumente"))
        self.menu_Personal = QtGui.QMenu(self.menubar)
        self.menu_Personal.setObjectName(_fromUtf8("menu_Personal"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.action_Lieferungen_Lieferungen = QtGui.QAction(MainWindow)
        self.action_Lieferungen_Lieferungen.setObjectName(_fromUtf8("action_Lieferungen_Lieferungen"))
        self.action_Lieferungen_Lieferanten = QtGui.QAction(MainWindow)
        self.action_Lieferungen_Lieferanten.setObjectName(_fromUtf8("action_Lieferungen_Lieferanten"))
        self.actionZoomIn = QtGui.QAction(MainWindow)
        self.actionZoomIn.setObjectName(_fromUtf8("actionZoomIn"))
        self.actionZoomOut = QtGui.QAction(MainWindow)
        self.actionZoomOut.setObjectName(_fromUtf8("actionZoomOut"))
        self.action_Report_Lager_Lagerstand = QtGui.QAction(MainWindow)
        self.action_Report_Lager_Lagerstand.setObjectName(_fromUtf8("action_Report_Lager_Lagerstand"))
        self.action_Report_Lager_MinimumLagerstand = QtGui.QAction(MainWindow)
        self.action_Report_Lager_MinimumLagerstand.setObjectName(_fromUtf8("action_Report_Lager_MinimumLagerstand"))
        self.action_Stammdaten_Perioden = QtGui.QAction(MainWindow)
        self.action_Stammdaten_Perioden.setObjectName(_fromUtf8("action_Stammdaten_Perioden"))
        self.action_Lieferungen_InitialerLagerstand = QtGui.QAction(MainWindow)
        self.action_Lieferungen_InitialerLagerstand.setObjectName(_fromUtf8("action_Lieferungen_InitialerLagerstand"))
        self.action_Report_Verbrauch_Artikel = QtGui.QAction(MainWindow)
        self.action_Report_Verbrauch_Artikel.setObjectName(_fromUtf8("action_Report_Verbrauch_Artikel"))
        self.actionAuf_wand = QtGui.QAction(MainWindow)
        self.actionAuf_wand.setObjectName(_fromUtf8("actionAuf_wand"))
        self.action_Report_Umsaetze_UmsatzTag = QtGui.QAction(MainWindow)
        self.action_Report_Umsaetze_UmsatzTag.setObjectName(_fromUtf8("action_Report_Umsaetze_UmsatzTag"))
        self.action_Report_Umsaetze_UmsatzAufwand = QtGui.QAction(MainWindow)
        self.action_Report_Umsaetze_UmsatzAufwand.setObjectName(_fromUtf8("action_Report_Umsaetze_UmsatzAufwand"))
        self.action_Report_Lager_Inventur = QtGui.QAction(MainWindow)
        self.action_Report_Lager_Inventur.setObjectName(_fromUtf8("action_Report_Lager_Inventur"))
        self.action_Stammdaten_Import = QtGui.QAction(MainWindow)
        self.action_Stammdaten_Import.setObjectName(_fromUtf8("action_Stammdaten_Import"))
        self.action_Report_Einkauf_GesamteLieferungen = QtGui.QAction(MainWindow)
        self.action_Report_Einkauf_GesamteLieferungen.setObjectName(_fromUtf8("action_Report_Einkauf_GesamteLieferungen"))
        self.action_Dokumente_Dokumenttypen = QtGui.QAction(MainWindow)
        self.action_Dokumente_Dokumenttypen.setObjectName(_fromUtf8("action_Dokumente_Dokumenttypen"))
        self.action_Dokumente_Dokumente = QtGui.QAction(MainWindow)
        self.action_Dokumente_Dokumente.setObjectName(_fromUtf8("action_Dokumente_Dokumente"))
        self.action_Stammdaten_Steuersaetze = QtGui.QAction(MainWindow)
        self.action_Stammdaten_Steuersaetze.setObjectName(_fromUtf8("action_Stammdaten_Steuersaetze"))
        self.action_Stammdaten_Liefereinheiten = QtGui.QAction(MainWindow)
        self.action_Stammdaten_Liefereinheiten.setObjectName(_fromUtf8("action_Stammdaten_Liefereinheiten"))
        self.action_Report_Umsaetze_AufwanddetailsProTag = QtGui.QAction(MainWindow)
        self.action_Report_Umsaetze_AufwanddetailsProTag.setObjectName(_fromUtf8("action_Report_Umsaetze_AufwanddetailsProTag"))
        self.action_Report_Umsaetze_DurchschUmsatzWochentag = QtGui.QAction(MainWindow)
        self.action_Report_Umsaetze_DurchschUmsatzWochentag.setObjectName(_fromUtf8("action_Report_Umsaetze_DurchschUmsatzWochentag"))
        self.action_Report_Einkauf_Verprobung = QtGui.QAction(MainWindow)
        self.action_Report_Einkauf_Verprobung.setObjectName(_fromUtf8("action_Report_Einkauf_Verprobung"))
        self.action_Personal_DienstplanErstellen = QtGui.QAction(MainWindow)
        self.action_Personal_DienstplanErstellen.setObjectName(_fromUtf8("action_Personal_DienstplanErstellen"))
        self.action_Personal_Dienstnehmer = QtGui.QAction(MainWindow)
        self.action_Personal_Dienstnehmer.setObjectName(_fromUtf8("action_Personal_Dienstnehmer"))
        self.action_Personal_Beschaeftigungsbereiche = QtGui.QAction(MainWindow)
        self.action_Personal_Beschaeftigungsbereiche.setObjectName(_fromUtf8("action_Personal_Beschaeftigungsbereiche"))
        self.action_Personal_Arbeitsplaetze = QtGui.QAction(MainWindow)
        self.action_Personal_Arbeitsplaetze.setObjectName(_fromUtf8("action_Personal_Arbeitsplaetze"))
        self.action_Stammdaten_Veranstaltungen = QtGui.QAction(MainWindow)
        self.action_Stammdaten_Veranstaltungen.setObjectName(_fromUtf8("action_Stammdaten_Veranstaltungen"))
        self.action_Report_Personal_DienstnehmerStunden = QtGui.QAction(MainWindow)
        self.action_Report_Personal_DienstnehmerStunden.setObjectName(_fromUtf8("action_Report_Personal_DienstnehmerStunden"))
        self.menuFile.addAction(self.actionQuit)
        self.menu_Einkauf.addAction(self.action_Report_Einkauf_GesamteLieferungen)
        self.menu_Einkauf.addAction(self.action_Report_Einkauf_Verprobung)
        self.menu_Umsaetze.addAction(self.action_Report_Umsaetze_UmsatzTag)
        self.menu_Umsaetze.addAction(self.action_Report_Umsaetze_UmsatzAufwand)
        self.menu_Umsaetze.addAction(self.action_Report_Umsaetze_AufwanddetailsProTag)
        self.menu_Umsaetze.addAction(self.action_Report_Umsaetze_DurchschUmsatzWochentag)
        self.menu_Verbrauch.addAction(self.action_Report_Verbrauch_Artikel)
        self.menu_Lagerstand.addAction(self.action_Report_Lager_Lagerstand)
        self.menu_Lagerstand.addAction(self.action_Report_Lager_MinimumLagerstand)
        self.menu_Lagerstand.addAction(self.action_Report_Lager_Inventur)
        self.menu_Personal_2.addAction(self.action_Report_Personal_DienstnehmerStunden)
        self.menu_Reports.addAction(self.menu_Lagerstand.menuAction())
        self.menu_Reports.addAction(self.menu_Verbrauch.menuAction())
        self.menu_Reports.addAction(self.menu_Umsaetze.menuAction())
        self.menu_Reports.addAction(self.menu_Einkauf.menuAction())
        self.menu_Reports.addAction(self.menu_Personal_2.menuAction())
        self.menu_Lieferungen.addAction(self.action_Lieferungen_Lieferungen)
        self.menu_Lieferungen.addAction(self.action_Lieferungen_Lieferanten)
        self.menu_Lieferungen.addAction(self.action_Lieferungen_InitialerLagerstand)
        self.menuStammdaten.addAction(self.action_Stammdaten_Perioden)
        self.menuStammdaten.addAction(self.action_Stammdaten_Import)
        self.menuStammdaten.addAction(self.action_Stammdaten_Steuersaetze)
        self.menuStammdaten.addAction(self.action_Stammdaten_Liefereinheiten)
        self.menuStammdaten.addAction(self.action_Stammdaten_Veranstaltungen)
        self.menu_Dokumente.addAction(self.action_Dokumente_Dokumenttypen)
        self.menu_Dokumente.addAction(self.action_Dokumente_Dokumente)
        self.menu_Personal.addAction(self.action_Personal_DienstplanErstellen)
        self.menu_Personal.addAction(self.action_Personal_Dienstnehmer)
        self.menu_Personal.addAction(self.action_Personal_Beschaeftigungsbereiche)
        self.menu_Personal.addAction(self.action_Personal_Arbeitsplaetze)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Reports.menuAction())
        self.menubar.addAction(self.menu_Lieferungen.menuAction())
        self.menubar.addAction(self.menu_Dokumente.menuAction())
        self.menubar.addAction(self.menu_Personal.menuAction())
        self.menubar.addAction(self.menuStammdaten.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuFile.setTitle(_translate("MainWindow", "&Datei", None))
        self.menu_Reports.setTitle(_translate("MainWindow", "&Reports", None))
        self.menu_Einkauf.setTitle(_translate("MainWindow", "&Einkauf", None))
        self.menu_Umsaetze.setTitle(_translate("MainWindow", "&Umsätze", None))
        self.menu_Verbrauch.setTitle(_translate("MainWindow", "&Verbrauch", None))
        self.menu_Lagerstand.setTitle(_translate("MainWindow", "&Lager", None))
        self.menu_Personal_2.setTitle(_translate("MainWindow", "&Personal", None))
        self.menu_Lieferungen.setTitle(_translate("MainWindow", "&Lieferungen", None))
        self.menuStammdaten.setTitle(_translate("MainWindow", "&Stammdaten", None))
        self.menu_Dokumente.setTitle(_translate("MainWindow", "Do&kumente", None))
        self.menu_Personal.setTitle(_translate("MainWindow", "&Personal", None))
        self.actionQuit.setText(_translate("MainWindow", "&Beenden", None))
        self.action_Lieferungen_Lieferungen.setText(_translate("MainWindow", "&Lieferungen", None))
        self.action_Lieferungen_Lieferanten.setText(_translate("MainWindow", "L&ieferanten", None))
        self.actionZoomIn.setText(_translate("MainWindow", "&Vergrößern", None))
        self.actionZoomIn.setToolTip(_translate("MainWindow", "Vergrößern", None))
        self.actionZoomOut.setText(_translate("MainWindow", "Verkleinern", None))
        self.actionZoomOut.setToolTip(_translate("MainWindow", "Verkleinern", None))
        self.action_Report_Lager_Lagerstand.setText(_translate("MainWindow", "&Lagerstand", None))
        self.action_Report_Lager_MinimumLagerstand.setText(_translate("MainWindow", "&Minimum erreicht", None))
        self.action_Stammdaten_Perioden.setText(_translate("MainWindow", "&Perioden", None))
        self.action_Lieferungen_InitialerLagerstand.setText(_translate("MainWindow", "Initialer Lager&stand", None))
        self.action_Report_Verbrauch_Artikel.setText(_translate("MainWindow", "&Artikel", None))
        self.actionAuf_wand.setText(_translate("MainWindow", "Auf&wand", None))
        self.action_Report_Umsaetze_UmsatzTag.setText(_translate("MainWindow", "&Umsatz/Tag", None))
        self.action_Report_Umsaetze_UmsatzAufwand.setText(_translate("MainWindow", "Umsatz:&Aufwand", None))
        self.action_Report_Lager_Inventur.setText(_translate("MainWindow", "&Inventur", None))
        self.action_Stammdaten_Import.setText(_translate("MainWindow", "&Import", None))
        self.action_Report_Einkauf_GesamteLieferungen.setText(_translate("MainWindow", "&Gesamte Lieferungen", None))
        self.action_Dokumente_Dokumenttypen.setText(_translate("MainWindow", "Dokument&typen", None))
        self.action_Dokumente_Dokumente.setText(_translate("MainWindow", "&Dokumente", None))
        self.action_Stammdaten_Steuersaetze.setText(_translate("MainWindow", "&Steuersätze", None))
        self.action_Stammdaten_Liefereinheiten.setText(_translate("MainWindow", "&Liefereinheiten", None))
        self.action_Report_Umsaetze_AufwanddetailsProTag.setText(_translate("MainWindow", "Aufwanddetails/&Tag", None))
        self.action_Report_Umsaetze_DurchschUmsatzWochentag.setText(_translate("MainWindow", "&Durchsch. Umsatz/Wochentag", None))
        self.action_Report_Einkauf_Verprobung.setText(_translate("MainWindow", "&Verprobung", None))
        self.action_Personal_DienstplanErstellen.setText(_translate("MainWindow", "Dienstplan &erstellen", None))
        self.action_Personal_Dienstnehmer.setText(_translate("MainWindow", "&Dienstnehmer", None))
        self.action_Personal_Beschaeftigungsbereiche.setText(_translate("MainWindow", "&Beschäftigungsbereiche", None))
        self.action_Personal_Arbeitsplaetze.setText(_translate("MainWindow", "&Arbeitsplätze", None))
        self.action_Stammdaten_Veranstaltungen.setText(_translate("MainWindow", "&Veranstaltungen", None))
        self.action_Report_Personal_DienstnehmerStunden.setText(_translate("MainWindow", "Dienstnehmer &Stunden", None))

