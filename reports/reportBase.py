from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
from DBConnection import dbConn

class ReportBase(QtGui.QWidget):
    
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        
        self.currentPeriod = 0
        
        self.connectToDb()
        self.setupUi()
        self.setupSignals()
        
    
    def setupUi(self):
        self.ui = self.uiClass()
        self.ui.setupUi(self)
        self.populatePeriodCB()
        
        
    def setupSignals(self):
        #self.populatePeriodCB()
        self.connect(self.ui.comboBox_period, QtCore.SIGNAL('currentIndexChanged(int)'), lambda: self.updatePeriod(self._getCurrentPeriodId()))

        
    def connectToDb(self):
        self.db = dbConn
            
            
    def populatePeriodCB(self):
        query = "select periode_id, periode_bezeichnung from perioden order by periode_bezeichnung desc"
        results = self.db.exec_(query)
    
        while results.next():
            id_ = results.value(0).toInt()[0]
            name = results.value(1).toString()
            self.ui.comboBox_period.addItem(name, QtCore.QVariant(int(id_)))
            #for reports that can compare two periods
            if hasattr(self.ui, 'comboBox_period2'):
                self.ui.comboBox_period2.addItem(name, QtCore.QVariant(int(id_)))
            
    def _getCurrentPeriodId(self):
        return self.ui.comboBox_period.itemData(self.ui.comboBox_period.currentIndex()).toInt()[0]
    
    def _getCurrentPeriodStartEnd(self):
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
        
        query.exec_("call sp_getPeriodStartEnd(%s, @pStart, @pEnd)" % self._getCurrentPeriodId())
        
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
    
            
    def updatePeriod(self, p):
        print 'ReportBase:updatePeriod', p
        self.currentPeriod = p
        self.updateData()
        
        
    def closeEvent(self, event):
        parent = self.parent()
        while parent:
            if isinstance(parent, QtGui.QMainWindow):
                parent.deregisterWindow(self)
                break
            else:
                parent = parent.parent()
                
        super(ReportBase, self).closeEvent(event)
        
        
    def getPurchasePrice(self, artikelBez, maxDate=None):
        query = 'select getPurchasePrice("%s", %s, %s)' % (artikelBez, self._getCurrentPeriodId(), 'NULL' if maxDate is None else "%s" % maxDate.isoformat())
        results = self.db.exec_(query)
        results.next()
        return results.value(0).toFloat()[0]