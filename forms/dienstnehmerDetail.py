# -*- coding: utf-8 -*-

from __future__ import print_function

#import datetime
import codecs

from PyQt4 import QtCore, QtGui, QtSql

from forms.formBase import FormBase
from ui.forms.dienstnehmerDetailForm_gui import Ui_DienstnehmerDetailForm

import config
from CONSTANTS import *
import DBConnection

import lib.datetimehelper

#from lib.NullDelegate import NullDelegate
#from lib.ImageViewer import ImageViewer
#from lib.ClickableLabel import ClickableLabel
from lib.Dienstnehmer import Dienstnehmer
#from lib.DienstnehmerEreignis import DienstnehmerEreignis



class DienstnehmerDetailForm(FormBase):

    uiClass = Ui_DienstnehmerDetailForm
    ident = 'dienstnehmerDetail'

    def __init__(self, parent):
        FormBase.__init__(self, parent)
        self.dienstnehmer = None
        

    def setupUi(self):
        super(DienstnehmerDetailForm, self).setupUi()

        self.ereignisModel = QtSql.QSqlRelationalTableModel()
        self.ereignisModel.setTable('dienstnehmer_ereignisse')
        #self.ereignisModel.setRelation(self.ereignisModel.fieldIndex('dir_dinid'), QtSql.QSqlRelation('dienstnehmer', 'din_id', 'din_nachname'))
        self.ereignisModel.setRelation(self.ereignisModel.fieldIndex('dir_ditid'), QtSql.QSqlRelation('dir_typen', 'dit_id', 'dit_kbez'))
        self.ereignisModel.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)  #see problem https://www.qtcentre.org/threads/59244-Changing-index-in-combobox-delegate-only-calls-setModelData-after-losing-focus
        self.ereignisModel.sort(self.ereignisModel.fieldIndex('dir_datum'), QtCore.Qt.AscendingOrder)
#        self.updateEreignisFilter()

        self.ereignisTableView = self.ui.tableView_ereignisse
        self.ereignisTableView.setModel(self.ereignisModel)
        
        delegate = QtSql.QSqlRelationalDelegate(self.ereignisTableView)
        # need to submit manually, since we have OnManualSubmit
        self.connect(delegate, QtCore.SIGNAL("closeEditor(QWidget*, QAbstractItemDelegate::EndEditHint)"), lambda editor, hint: self.ereignisModel.submitAll())
        self.ereignisTableView.setItemDelegate(delegate)
        
        self.ereignisTableView.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.ereignisTableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.ereignisTableView.setColumnHidden(self.ereignisModel.fieldIndex('dir_id'), True)
        self.ereignisTableView.setColumnHidden(self.ereignisModel.fieldIndex('dir_dinid'), True)
        self.ereignisTableView.resizeColumnsToContents()
        self.ereignisTableView.horizontalHeader().setStretchLastSection(True)
        
        
        self.bereichModel = QtSql.QSqlRelationalTableModel()
        self.bereichModel.setTable('beschaeftigungsbereiche')
        self.bereichModel.select()
        self.ui.comboBox_bereich.setModel(self.bereichModel)
        self.ui.comboBox_bereich.setModelColumn(self.bereichModel.fieldIndex('beb_bezeichnung'))
        
        self.gehaltModel = QtSql.QSqlRelationalTableModel()
        self.gehaltModel.setTable('gehaelter')
        self.gehaltModel.select()
        self.ui.comboBox_gehalt.setModel(self.gehaltModel)
        self.ui.comboBox_gehalt.setModelColumn(self.gehaltModel.fieldIndex('geh_kbez'))
        
        
    @property
    def dinId(self):
        return self._dinId
        
    @dinId.setter
    def dinId(self, val):
        self._dinId = val
        self.updateEreignisFilter()

#		self.createContextMenu()


    def setupSignals(self):
        #super(DienstnehmerDetailForm, self).setupSignals()
        self.connect(self.ui.pushButton_newEreignis, QtCore.SIGNAL('clicked()'), self.addEreignis)
        self.connect(self.ui.pushButton_deleteEreignis, QtCore.SIGNAL('clicked()'), self.deleteEreignis)
        self.connect(self.ui.pushButton_color, QtCore.SIGNAL('clicked()'), self.changeColor)
        #self.connect(self.ui.lineEdit_dokId, QtCore.SIGNAL('textChanged (const QString&)'), self.displayImageFromDb)
        #self.connect(self.ui.label_document, QtCore.SIGNAL('clicked()'), self.showImage)
#		self.connect(self.ereignisModel, QtCore.SIGNAL('dataChanged(const QModelIndex&,const QModelIndex&)'), self.articleChanged)
#		self.connect(self.ui.tableView_ereignisse.selectionModel(), QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'), self.detailSelectionChanged)


    def load(self):
        self.dienstnehmer = dn = Dienstnehmer()
        if self.dinId is not None:
            self.dienstnehmer.get(self.dinId)
            u = self.ui
            
            u.lineEdit_nummer.setText(dn['din_nummer'])
            u.lineEdit_svnr.setText(dn['din_svnr'])
            u.lineEdit_nachname.setText(dn['din_nachname'])
            u.lineEdit_vorname.setText(dn['din_vorname'])
            u.doubleSpinBox_maxLohn.setValue(dn['din_gehalt'])

            #idx = self.bereichModel.match(self.bereichModel.index(0, self.bereichModel.fieldIndex('beb_id')), QtCore.Qt.DisplayRole, dn['din_bebid'])[0]
            idx = self.getComboboxIdxForPK(u.comboBox_bereich, 'beb_id', dn['din_bebid'])
            u.comboBox_bereich.setCurrentIndex(idx.row())

            #idx = self.gehaltModel.match(self.gehaltModel.index(0, self.gehaltModel.fieldIndex('geh_id')), QtCore.Qt.DisplayRole, dn['din_gehid'])[0]
            idx = self.getComboboxIdxForPK(u.comboBox_gehalt, 'geh_id', dn['din_gehid'])
            u.comboBox_gehalt.setCurrentIndex(idx.row())
            
            self.setButtonColor()
        
        
    def changeColor(self):
        print("changeColor")
        self.dienstnehmer['din_farbe'] = QtGui.QColorDialog.getColor().name()
        self.setButtonColor()
        
    def setButtonColor(self):
        self.ui.pushButton_color.setStyleSheet('background-color:'+self.dienstnehmer['din_farbe']+';')


    def validateAndSave(self):
        if self.dienstnehmer is None:
            self.dienstnehmer = Dienstnehmer()
            
        dn = self.dienstnehmer
        u = self.ui
        
        dn['din_nummer'] = u.lineEdit_nummer.text()
        dn['din_svnr'] = u.lineEdit_svnr.text()
        dn['din_nachname'] = u.lineEdit_nachname.text()
        dn['din_vorname'] = u.lineEdit_vorname.text()
        dn['din_gehalt'] = u.doubleSpinBox_maxLohn.value()
        dn['din_bebid'] = self.getPKForCombobox(u.comboBox_bereich, 'beb_id')
        dn['din_gehid'] = self.getPKForCombobox(u.comboBox_gehalt, 'geh_id')
        
        try:
            dn.validate()
        except ValueError as e:
            QtGui.QMessageBox.critical(self, u'Validierung fehlgeschlagen', unicode(e))
            return False
            
        dn.save()
        dn.clearQueryCache()
            
        return True


    def accept(self):
        if self.validateAndSave():
            try:
                self.dienstnehmer.validateEreignisse()
            except LookupError as e:
                QtGui.QMessageBox.critical(self, u'Fehlendes Ereignis', unicode(e))
                return False
            
            super(DienstnehmerDetailForm, self).accept()
        else:
            return False

    def reject(self):
        super(DienstnehmerDetailForm, self).reject()


    def addEreignis(self, artikelId=None, anzahl=None, einkaufspreis=None, stsId=None):
        if self.validateAndSave():
            r = self.ereignisModel.record()
            print(self.dienstnehmer)
            r.setValue('dir_dinid', self.dienstnehmer['din_id'])
            r.setValue('dir_datum', QtCore.QDateTime(lib.datetimehelper.today()))
            self.ereignisModel.insertRecord(-1, r)
#            self.ereignisModel.select()
            #self.ereignisModel.submitAll()


    def deleteEreignis(self):
        selected = self.ereignisTableView.selectionModel().selectedRows()
        for i in range(len(selected)):
            self.ereignisModel.removeRows(selected[i].row(), 1)
        self.ereignisModel.submitAll()


    def updateEreignisFilter(self):
        self.ereignisModel.setFilter('dir_dinid = %s' % self.dinId)
        self.ereignisModel.select()

