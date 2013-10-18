# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from DBConnection import dbConn


class FormBase(QtGui.QDialog):
    
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        
        self.currentPeriod = -1
        
        self.connectToDb()
        self.setupUi()
        self.setupSignals()
        
    def connectToDb(self):
        self.db = dbConn
        
    def setupUi(self):
        self.ui = self.uiClass()
        self.ui.setupUi(self)
    
    def setupSignals(self):
        try:
            self.connect(self.ui.comboBox_period,
                         QtCore.SIGNAL('currentIndexChanged(int)'),
                         lambda: self.updatePeriod(self.getCurrentPeriodId()))
            self.populatePeriodCB()
        except AttributeError:
            pass
    
    def populatePeriodCB(self):
        query = "select periode_id, periode_bezeichnung \
                 from perioden \
                 order by periode_bezeichnung desc"
        results = self.db.exec_(query)
    
        while results.next():
            id_ = results.value(0).toInt()[0]
            name = results.value(1).toString()
            self.ui.comboBox_period.addItem(name, QtCore.QVariant(int(id_)))
            
    def getCurrentPeriodId(self):
        return self.ui.comboBox_period.itemData(self.ui.comboBox_period.currentIndex()).toInt()[0]
    
    def getCheckpointIdForPeriod(self, periodId):
        query = QtSql.QSqlQuery()
        query.prepare("""select periode_checkpoint_jahr from perioden where periode_id = ?""")
        query.addBindValue(periodId)
        query.exec_()
        query.next()
        id_ = query.value(0)
        if id_.isNull():
            return None
        else:
            return id_.toInt()[0]
        
    def getCurrentPeriodStartEnd(self):
        query = QtSql.QSqlQuery()
        
        query.prepare("select periode_start, periode_ende from perioden where periode_id = ?")
        query.bindValue(0, self.getCurrentPeriodId())
        
        query.exec_()
    
        query.next()
        start = query.value(0).toDate().toPyDate()
        end = query.value(1).toDate().toPyDate()
            
        return start, end
    
    def getPKForCombobox(self, combo, pkName):
        model = combo.model()
        row = combo.currentIndex()
        col = model.fieldIndex(pkName)
        index = model.index(row, col)
        pk = model.data(index).toInt()[0]
        return pk
    
    @property
    def cfgKey(self):
        return 'form_' + self.ident
    
    def updatePeriod(self, p):
        self.currentPeriod = p
        
    def beginTransaction(self):
        QtSql.QSqlDatabase.database().transaction()
        
    def commit(self):
        QtSql.QSqlDatabase.database().commit()
        
    def rollback(self):
        QtSql.QSqlDatabase.database().rollback()
        
    def closeEvent(self, event):
        parent = self.parent()
        while parent:
            if isinstance(parent, QtGui.QMainWindow):
                parent.deregisterWindow(self)
                break
            else:
                parent = parent.parent()
                
        super(FormBase, self).closeEvent(event)
