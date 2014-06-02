# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection
import config

from forms.formBase import FormBase
from ui.forms.dienstnehmerEreignisseForm_gui import Ui_DienstnehmerEreignisseForm

class DienstnehmerEreignisseForm(FormBase):
    
    uiClass = Ui_DienstnehmerEreignisseForm
    ident = 'dienstnehmer_ereignisse'
    
    def setupUi(self):
        super(DienstnehmerEreignisseForm, self).setupUi()
        
        self.model = QtSql.QSqlRelationalTableModel()
        self.model.setTable('dienstnehmer_ereignisse')
        
        #the a record before setting the relations for use in the newRecord method
        self.baseRecord = self.model.record()
        
        self.model.setRelation(self.model.fieldIndex('dir_dinid'), QtSql.QSqlRelation('dienstnehmer', 'din_id', 'din_name'))
        self.model.setRelation(self.model.fieldIndex('dir_ditid'), QtSql.QSqlRelation('dir_typen', 'dit_id', 'dit_kbez'))
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        
        # column headers
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, u'ID')
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, u'Dienstnehmer')
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, u'Datum')
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, u'Typ')
        

        
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
        
        self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self.newRecord)
        self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self.deleteRecord)
        
    
    def newRecord(self, dinId=None, ditId=None):
        if dinId is None:
            query = QtSql.QSqlQuery()
            query.prepare("""select min(din_id) from dienstnehmer""")
            query.exec_()
            query.next()
            dinId = query.value(0).toInt()[0]
        
        if ditId is None:
            query = QtSql.QSqlQuery()
            query.prepare("""select min(dit_id) from dir_typen""")
            query.exec_()
            query.next()
            ditId = query.value(0).toInt()[0]

        rec = self.baseRecord
        rec.setValue(1, dinId)
        rec.setValue(2, '')
        rec.setValue(3, ditId)
        self.model.insertRecord(-1, rec)
        
        
    def deleteRecord(self):
        """selected = self.tableView.selectionModel().selectedRows(0);
        print selected
        for i in range(len(selected)):
            self.model.removeRows(selected[i].row(), 1);"""
        self.model.removeRows(self.currentSourceIndex().row(), 1)
        self.model.submitAll()
        
    def currentSourceIndex(self):
        """maps the current selection to the index of the proxy's current source"""
        idx = self.ui.tableView.selectionModel().currentIndex()#.row()
        idx = self.ui.tableView.model().mapToSource(idx)
        return idx
    
