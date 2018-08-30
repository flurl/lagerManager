# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtSql

from lib.LMDatabaseObject import LMDatabaseObject
from lib.LMDatabaseRelation import LMDatabaseRelation

class DienstnehmerEreignis(LMDatabaseObject):

    _DBTable = 'dienstnehmer_ereignisse'
    #	_dynamicColumns = {'stundensatz':'getHourlyWage'}
    dienstnehmer = LMDatabaseRelation('dir_dinid', 'lib.Dienstnehmer.Dienstnehmer')
    typ = LMDatabaseRelation('dir_ditid', 'lib.DienstnehmerEreignisTyp.DienstnehmerEreignisTyp')
    
    def __unicode__(self):
        return unicode(self['dir_datum'].toPyDateTime().isoformat()) + u' - ' + unicode(self['dienstnehmer']) + ': ' + unicode(self['typ'])
        
    def __str__(self):
        return unicode(self).encode('utf-8')
        
    def getAntipode(self):
        ditBeginnDitId = self['typ']['dit_beginn_ditid']
        ditEndeDitId = self['typ']['dit_ende_ditid']
        if ditBeginnDitId > 0:
            found = ''
            query = QtSql.QSqlQuery()
            query.prepare("""select dir_id, dir_ditid
                             from dienstnehmer_ereignisse
                             where 1=1
                             and dir_dinid = ?
                             and dir_ditid in (?, ?)
                             and dir_datum {operator} ?
                             order by dir_datum {order}
                             limit 1""".format({'operator': '<' if ditBeginnDitId > 0 else '<', 'order': 'desc' if ditBeginnDitId > 0 else 'asc'}))
            query.addBindValue(self['dir_dinid'])
            query.addBindValue(self['typ']['dit_id'])
            query.addBindValue(ditBeginnDitId if ditBeginnDitId > 0 else ditEndeDitId)
            query.addBindValue(self['dir_datum'])
            query.exec_()
            if query.lastError().isValid():
                print 'SQL error:', query.lastError().text()
                QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
                query.lastError().text())
            found = False
            while query.next():
                if query.value(1).toInt()[0] == (ditBeginnDitId if ditBeginnDitId > 0 else ditEndeDitId):
                    found = query.value(0).toInt()[0]
            if found:
                return lib.DienstnehmerEreignis.DienstnehmerEreignis(found)
            else:
                return None
                
        


if __name__ == '__main__':
    import sys
    import DBConnection
    import lib.Dienstnehmer
#    import lib.DienstnehmerEreignisTyp
    print sys.argv
    DBConnection.connect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    
    dbObj = DienstnehmerEreignis()
    dbObj.get(48)
    while dbObj.next():
        print dbObj
        print dbObj.getAntipode()
        print (("*"*20)+'\n')*5
        
    dbObj.get(25)
    print dbObj
    print dbObj.getAntipode()

    """
    dn = lib.Dienstnehmer.Dienstnehmer(21)
    ereignisse = DienstnehmerEreignis().find('dir_dinid', dn['din_id'])
    while ereignisse.next():
        print ereignisse"""
        
        
import lib.Dienstnehmer
import lib.DienstnehmerEreignisTyp
