# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection
import config

from forms.formBase import FormBase
from ui.forms.ekModifikatorenForm_gui import Ui_EkModifikatorenForm

class EkModifikatorenForm(FormBase):
    
    uiClass = Ui_EkModifikatorenForm
    ident = 'ek_modifikatoren'
    
    def setupUi(self):
        super(EkModifikatorenForm, self).setupUi()
        
        self.model = QtSql.QSqlRelationalTableModel()
        self.model.setTable('ek_modifikatoren')
        
        #the a record before setting the relations for use in the newRecord method
        self.baseRecord = self.model.record()
        
        self.model.setRelation(self.model.fieldIndex('emo_artikel_id'), QtSql.QSqlRelation('artikel_basis', 'artikel_id', 'artikel_bezeichnung'))
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        
        self.setFilter()
        
        # column headers
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, u'ID')
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, u'Artikel')
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, u'Operation')
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, u'Modifikator')
        

        
        # table view
        # ------------------------------------------------
        self.tableView = self.ui.tableView
        self.tableView.setModel(self.model)
        self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
        self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setSortingEnabled(True)
        
        self.tableView.setColumnHidden(self.model.fieldIndex('emo_periode_id'), True)
        
        self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
        self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)
        self.connect(self.ui.comboBox_period, QtCore.SIGNAL('currentIndexChanged(int)'), self.setFilter)
        
    
    def newRecord(self):
        rec = self.baseRecord
        #rec.setValue(1, nId)
        #rec.setValue(2, '')
        rec.setValue(4, self.getCurrentPeriodId())
        self.model.insertRecord(-1, rec)
        
        
    def deleteRecord(self):
        self.model.removeRows(self.currentSourceIndex(self.ui.tableView).row(), 1)
        self.model.submitAll()


    def setFilter(self):
        self.model.setFilter('emo_periode_id=%(perId)s and artikel_periode=%(perId)s'%{'perId':self.getCurrentPeriodId()})
        self.model.select()

