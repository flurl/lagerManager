# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from DBConnection import dbConn
import config 


class ComboBoxPKError(Exception):
    pass


class LMBase(QtGui.QDialog):
    
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
    
    def _getCurrentPeriodId(self):
        return self.getCurrentPeriodId()
    
    
    def getCheckpointIdForPeriod(self, periodId):
        query = QtSql.QSqlQuery()
        query.prepare("""select periode_checkpoint_jahr from perioden where periode_id = ?""")
        query.addBindValue(periodId)
        query.exec_()
        query.next()
        id_ = query.value(0)
        if id_.isNull() or id_.toInt()[0] == 0:
            return None
        else:
            return id_.toInt()[0]
        
    def getCurrentPeriodStartEnd(self):
        """returns the start and end datetime for the current period
        
        this looks like a mess, but there are two things to consider:
        1) qt can't access OUT and INOUT params for stored procedures directly via QSqlQuery::boundValue(). 
           This means we need the second select query (see http://doc.qt.io/qt-4.8/sql-driver.html#qmysql-for-mysql-4-and-higher)
           
        2) MySQL user variables can be assigned a value from a limited set of data types: integer, decimal, 
           floating-point, binary or nonbinary string, or NULL value. A value of a type other than one 
           of the permissible types is converted to a permissible type (see https://dev.mysql.com/doc/refman/5.0/en/user-variables.html)
           That's the reason for the whole string parsing down there.
        """
        
        query = QtSql.QSqlQuery()
        
        query.exec_("call sp_getPeriodStartEnd(%s, @pStart, @pEnd)" % self.getCurrentPeriodId())
        
        if query.lastError().isValid():
            print "Error executing query: ", query.lastQuery(), query.executedQuery(), query.lastError().text()
        
        query.exec_("select @pStart, @pEnd")
        if query.lastError().isValid():
            print "Error executing query: ", query.lastQuery(), query.executedQuery(), query.lastError().text()
        
        query.next()
        start = QtCore.QDateTime.fromString(query.value(0).toString(), "yyyy-MM-dd HH:mm:ss").toPyDateTime()
        end = QtCore.QDateTime.fromString(query.value(1).toString(), "yyyy-MM-dd HH:mm:ss").toPyDateTime()
        
        print "start, end: ", start, end
            
        return start, end
    
    def _getCurrentPeriodStartEnd(self):
        return self.getCurrentPeriodStartEnd()
    
    
    def getPKForCombobox(self, combo, pkName):
        model = combo.model()
        row = combo.currentIndex()
        if row == -1:
            raise ComboBoxPKError()
        if isinstance(pkName, int):
            col = pkName
        else:
            col = model.fieldIndex(pkName)
        index = model.index(row, col)
        pk = model.data(index).toInt()[0]
        return pk
    
    #@property
    #def cfgKey(self):
        #return 'form_' + self.ident
        
    def getConfig(self):
        cfgKey = self.cfgKey
        
        try:
            cfg  = config.config[cfgKey]
        except KeyError:
            config.config[cfgKey] = {}
            cfg  = config.config[cfgKey]
        
        return cfg
    
    
    def saveConfig(self):
        config.config.write()
    
    
    def updatePeriod(self, p):
        self.currentPeriod = p
        
    def beginTransaction(self):
        QtSql.QSqlDatabase.database().transaction()
        
    def commit(self):
        QtSql.QSqlDatabase.database().commit()
        
    def rollback(self):
        QtSql.QSqlDatabase.database().rollback()
        
    def showEvent(self, event):
        self.restoreWindowGeometry()
        super(LMBase, self).showEvent(event)
        
    def deregisterWindow(self):
        parent = self.parent()
        while parent:
            if isinstance(parent, QtGui.QMainWindow):
                parent.deregisterWindow(self)
                break
            else:
                parent = parent.parent()
        
        
    def saveWindowGeometry(self):
        cfgKey = self.cfgKey
        
        try:
            cfg  = config.config[cfgKey]
        except KeyError:
            config.config[cfgKey] = {}
            cfg  = config.config[cfgKey]
        
        if self.parentWidget().metaObject().className() == 'QMdiSubWindow':
            win = self.parentWidget()
        else:
            win = self
        
        cfg['geometry'] = (win.x(), win.y(), win.width(), win.height())
        config.config.write()
        
    def restoreWindowGeometry(self):
        try:
            geometry = config.config[self.cfgKey]['geometry']
        except KeyError:
            return
        
        if self.parentWidget().metaObject().className() == 'QMdiSubWindow':
            win = self.parentWidget()
        else:
            win = self
            
        win.resize(int(geometry[2]),int(geometry[3]))
            
    def accept(self):
        self.saveWindowGeometry()
        self.deregisterWindow()
        super(LMBase, self).accept()

    def reject(self):
        self.saveWindowGeometry()
        self.deregisterWindow()
        super(LMBase, self).reject()
        
    def currentSourceIndex(self, tableView):
        """maps the current selection to the index of the proxy's current source"""
        idx = tableView.selectionModel().currentIndex()#.row()
        # if no proxy model is used, call to mapToSource will fail
        try:
            idx = tableView.model().mapToSource(idx)
        except AttributeError:
            pass
        return idx
    
    def closeEvent(self, event):
        parent = self.parent()
        while parent:
            if isinstance(parent, QtGui.QMainWindow):
                parent.deregisterWindow(self)
                break
            else:
                parent = parent.parent()
                
        super(LMBase, self).closeEvent(event)
        
        
    def getPurchasePrice(self, artikelBez, maxDate=None):
        query = 'select getPurchasePrice("%s", %s, %s)' % (artikelBez, self._getCurrentPeriodId(), 'NULL' if maxDate is None else "\"%s\"" % maxDate.isoformat())
        results = self.db.exec_(query)
        results.next()
        return results.value(0).toFloat()[0]
 
