#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import importlib

from PyQt4 import QtCore, QtGui

from ui.lagerManagerMainWindow_gui import Ui_MainWindow
#from CONSTANTS import *
import DBConnection
import lagerManager_rc  # @UnusedImport
import Updater
from lib.GlobalConfig import globalConf


from version import VERSION


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        self.openWindows = {}
        self.__tabbedView = False

        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._setupForm()
        self.openConnectDlg()

        splash.show()
        self.checkDbUpdate()

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window,
                         QtGui.QColor(globalConf['baseColor']))
        self.setPalette(palette)

        self.statusBar().addPermanentWidget(
                                        QtGui.QLabel('V' + unicode(VERSION)),
                                        1)
        self.statusBar().addPermanentWidget(
                                        QtGui.QLabel('Verbindung: ' +
                                                    DBConnection.connName))

    def _setupForm(self):
        self.connect(self.ui.actionQuit,
                    QtCore.SIGNAL('triggered()'),
                    self.close)

        self.connect(self.ui.action_Report_Lager_Lagerstand,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.lagerstand.LagerstandReport'))
        self.connect(self.ui.action_Report_Lager_AktuellerLagerstand,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.lagerstandTextuell.LagerstandTextuellReport'))
        self.connect(self.ui.action_Report_Lager_MinimumLagerstand,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.minimumLagerstand.MinimumLagerstandReport'))
        self.connect(self.ui.action_Report_Lager_Inventur,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.inventur.InventurReport'))
        self.connect(self.ui.action_Report_Verbrauch_Artikel,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.verbrauch.VerbrauchReport'))
        self.connect(self.ui.action_Report_Verbrauch_AktuellerVerbrauch,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.verbrauchTextuell.VerbrauchTextuellReport'))
        self.connect(self.ui.action_Report_Umsaetze_UmsatzTag,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.umsatzProTag.UmsatzProTagReport'))
        self.connect(self.ui.action_Report_Umsaetze_UmsatzAufwand,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.umsatzAufwand.UmsatzAufwandReport'))
        self.connect(self.ui.action_Report_Umsaetze_AufwanddetailsProTag,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.aufwandDetailsProTag.AufwandDetailsProTagReport'))
        self.connect(self.ui.action_Report_Umsaetze_DurchschUmsatzWochentag,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.durchschnittUmsatzProTag.DurchschnittUmsatzProTagReport'))
        self.connect(self.ui.action_Report_Umsaetze_VerkaufteArtikel,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.verkaufteArtikel.VerkaufteArtikelReport'))
        self.connect(self.ui.action_Report_Umsaetze_RechnungenStatistik,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.rechnungenStatistik.RechnungenStatistikReport'))
        self.connect(self.ui.action_Report_Einkauf_GesamteLieferungen,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.gesamteLieferungen.GesamteLieferungenReport'))
        self.connect(self.ui.action_Report_Einkauf_Verprobung,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.verprobung.VerprobungReport'))
        self.connect(self.ui.action_Report_Personal_DienstnehmerStunden,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.dienstnehmerStunden.DienstnehmerStundenReport'))
        self.connect(self.ui.action_Report_Personal_Bonierzeiten,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.bonierzeiten.Bonierzeiten'))
        self.connect(self.ui.action_Report_Artikel_Rezepturen,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.rezepturen.RezepturenReport'))
        self.connect(self.ui.action_Report_Artikel_NichtVorhandene,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('reports.nichtVorhandeneBonierteArtikel.NichtVorhandeneBonierteArtikelReport'))

        self.connect(self.ui.action_Lieferungen_Lieferungen,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.lieferung.LieferungForm'))
        self.connect(self.ui.action_Lieferungen_Lieferanten,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.lieferanten.LieferantenForm'))
        self.connect(self.ui.action_Lieferungen_InitialerLagerstand,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.lagerstand.LagerstandForm'))

        self.connect(self.ui.action_Dokumente_Dokumenttypen,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.dokumenttypen.DokumenttypenForm'))
        self.connect(self.ui.action_Dokumente_Dokumente,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.dokumente.DokumenteForm'))

        self.connect(self.ui.action_Personal_DienstplanErstellen,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.dienstplan.DienstplanForm', 'dlg'))
        self.connect(self.ui.action_Personal_Beschaeftigungsbereiche,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.beschaeftigungsbereiche.BeschaeftigungsbereicheForm'))
        self.connect(self.ui.action_Personal_Arbeitsplaetze,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.arbeitsplaetze.ArbeitsplaetzeForm'))
        self.connect(self.ui.action_Personal_Dienstnehmer,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.dienstnehmer.DienstnehmerForm'))
        self.connect(self.ui.action_Personal_DienstnehmerEreignisse,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.dienstnehmerEreignisse.DienstnehmerEreignisseForm'))
        self.connect(self.ui.action_Personal_Gehaelter,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.gehaelter.GehaelterForm'))
        self.connect(self.ui.action_Personal_Loehne,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.loehne.LoehneForm'))

        self.connect(self.ui.action_Stammdaten_Perioden,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('periodenDlg.PeriodenDialog', 'dlg'))
        self.connect(self.ui.action_Stammdaten_Import,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.dbImport.ImportForm'))
        self.connect(self.ui.action_Stammdaten_Steuersaetze,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.steuersaetze.SteuersaetzeForm'))
        self.connect(self.ui.action_Stammdaten_Liefereinheiten,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.liefereinheiten.LiefereinheitenForm'))
        self.connect(self.ui.action_Stammdaten_Veranstaltungen,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.veranstaltungen.VeranstaltungenForm'))
        self.connect(self.ui.action_Stammdaten_Buchungskonten,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.buchungskonten.BuchungskontenForm'))
        self.connect(self.ui.action_Stammdaten_DNEreignisTypen,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.dirTypen.DirTypenForm'))
        self.connect(self.ui.action_Stammdaten_Konfiguration,
                    QtCore.SIGNAL('triggered()'),
                    lambda: self.openWindow('forms.globalConfig.ConfigForm'))

    def openConnectDlg(self):
        import connectDlg
        form = connectDlg.ConnectDialog(self)
        form.exec_()

    def openWindow(self, name, type_='mdi'):
        if name in self.openWindows:
            if type_ == 'mdi':
                self.ui.mdiArea.setActiveSubWindow(
                                                self.openWindows[name].
                                                parent())
            else:
                self.openWindows[name].show()
        else:
            module = name.rpartition('.')[0]
            className = name.rpartition('.')[2]

            importlib.import_module(module)
            windowClass = getattr(sys.modules[module], className)
            window = windowClass(self)

            self.openWindows[name] = window
            self.openWindows[id(window)] = name

            if type_ == 'mdi':
                window = self.ui.mdiArea.addSubWindow(window)
                self.connect(window,
                            QtCore.SIGNAL('windowStateChanged(Qt::WindowStates, Qt::WindowStates)'),
                            self.subWindowStateChanged)

            window.setPalette(self.palette())
            window.show()

    def deregisterWindow(self, window):
        try:
            name = self.openWindows[id(window)]
            del self.openWindows[name]
            del self.openWindows[id(window)]
        except KeyError:
            print('window with id %s not found in open windows dict.' % id(window))

    def subWindowStateChanged(self, oldState, newState):
        if newState != oldState:
            if not self.__tabbedView and newState & QtCore.Qt.WindowMaximized:
                self.setTabbedView()

    def setTabbedView(self, enable=True):
        mdi = self.ui.mdiArea
        if enable and mdi.viewMode() != QtGui.QMdiArea.TabbedView:
            print 'enabling TabbedView'
            mdi.setViewMode(QtGui.QMdiArea.TabbedView)
            mdi.setDocumentMode(True)
            tabBar = mdi.findChildren(QtGui.QTabBar)[0]
            # tabBar.setTabsClosable(True)
            self.connect(tabBar,
                        QtCore.SIGNAL('currentChanged(int)'),
                        self.setTabButtons)
            self.setTabButtons()
            self.__tabbedView = True
        elif mdi.viewMode() != QtGui.QMdiArea.SubWindowView:
            print 'disabling TabbedView'
            mdi.setViewMode(QtGui.QMdiArea.SubWindowView)
            mdi.setDocumentMode(False)
            self.__tabbedView = False

    def setTabButtons(self, idx=None):
        tabBar = self.ui.mdiArea.findChildren(QtGui.QTabBar)[0]
        for idx in range(tabBar.count()):
            widget = QtGui.QWidget(self)
            layout = QtGui.QHBoxLayout()

            pix = (QtGui.QApplication.style().
                standardIcon(QtGui.QStyle.SP_TitleBarNormalButton))
            btn = QtGui.QPushButton(pix, u'')
            btn.setFixedSize(btn.iconSize().width(), btn.iconSize().height())
            self.connect(btn,
                        QtCore.SIGNAL('clicked()'),
                        lambda: self.setTabbedView(False))
            layout.addWidget(btn)

            pix = QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_TitleBarCloseButton)
            btn = QtGui.QPushButton(pix, u'')
            btn.setFixedSize(btn.iconSize().width(), btn.iconSize().height())

            self.ui.mdiArea.currentSubWindow()
            self.connect(btn,
                        QtCore.SIGNAL('clicked()'),
                        lambda tb=tabBar, i=idx: (tb.setCurrentIndex(i),
                                                self.ui.mdiArea.closeActiveSubWindow()))
            layout.addWidget(btn)

            widget.setLayout(layout)
            tabBar.setTabButton(idx, QtGui.QTabBar.RightSide, widget)

    def checkDbUpdate(self):
        splash.showMessage("checking for db updates")
        u = Updater.Updater()
        if u.checkForDatabaseUpdates():
            splash.showMessage(u'Installing updates')
            u.installDatabaseUpdates()
        splash.showMessage("update check finished")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    # Create and display the splash screen
    pixmap = QtGui.QPixmap(':/images/splashscreen.png')
    splash = QtGui.QSplashScreen(pixmap, QtCore.Qt.WindowStaysOnTopHint)

    win = MainWindow()
    win.show()

    splash.finish(win)

    sys.exit(app.exec_())
