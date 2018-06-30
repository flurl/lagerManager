# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.dienstnehmerEreignisseReport_gui import Ui_DienstnehmerEreignisse
from textReport import TextReport


from lib.GlobalConfig import globalConf
from CONSTANTS import *



class DienstnehmerEreignisseReport(TextReport):

    uiClass = Ui_DienstnehmerEreignisse
    ident = 'dienstnehmerEreignisse'

    def __init__(self, parent=None):
        TextReport.__init__(self, parent)

        self.setHeader('Dienstnehmer Ereignisse')
        self.setFooter('here could be a nice footer')
        
        #self.setTableHeaders([])

        self.updateData()
        
        
    def setupUi(self):
        super(DienstnehmerEreignisseReport, self).setupUi()

        model = QtSql.QSqlTableModel()
        model.setTable('dienstnehmer')
        model.select()

        self.ui.comboBox_employees.setModel(model)
        self.ui.comboBox_employees.setModelColumn(model.fieldIndex('din_name'))

        self.ui.comboBox_employees.insertSeparator(-1)
        self.ui.comboBox_employees.setCurrentIndex(-1)
        
    def setupSignals(self):
        super(DienstnehmerEreignisseReport, self).setupSignals()
        self.connect(self.ui.comboBox_employees, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
        self.connect(self.ui.checkBox_markOpen, QtCore.SIGNAL('stateChanged(int)'), self.updateData)
        self.connect(self.ui.checkBox_markOrphans, QtCore.SIGNAL('stateChanged(int)'), self.updateData)
        
    def updateData(self):
        query = self.mkQuery()
        if not self.ui.checkBox_markOpen.isChecked() and not self.ui.checkBox_markOrphans.isChecked():
            self.setData(query)
        else:
            data = []
            results = self.db.exec_(query)
            while results.next():
                dinId = results.value(0).toInt()[0]
                dinNr = results.value(1).toInt()[0]
                dinName = results.value(2).toString()
                dirDatum = results.value(3).toDateTime()
                ditKbez = results.value(4).toString()
                ditBeginnDitId = None if results.isNull(5) else results.value(5).toInt()[0]
                ditEndeDitId = None if results.isNull(6) else results.value(6).toInt()[0]
                ditId = results.value(7).toInt()[0]
                dirId = results.value(8).toInt()[0]
                
                found = ''
                if ditBeginnDitId is not None:
                    query = QtSql.QSqlQuery()
                    query.prepare("""select dir_id, dir_ditid
                                     from dienstnehmer_ereignisse
                                     where 1=1
                                     and dir_dinid = ?
                                     and dir_ditid in (?, ?)
                                     and dir_datum < ?
                                     order by dir_datum desc
                                     limit 1""")
                    query.addBindValue(dinId)
                    query.addBindValue(ditId)
                    query.addBindValue(ditBeginnDitId)
                    query.addBindValue(dirDatum)
                    query.exec_()
                    if query.lastError().isValid():
                        print 'SQL error:', query.lastError().text()
                        QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
                        query.lastError().text())
                    found = False
                    while query.next():
                        if query.value(1).toInt()[0] == ditBeginnDitId:
                            found = query.value(0).toInt()[0]
                data.append([d if found != False else (d, 'strong') for d in [dinNr, dinName, dirDatum.toPyDateTime(), ditKbez, found]])
        
            self.setData(data)
        
        self.process()
        
        
    def mkQuery(self):
        selectedEmpIdx = self.ui.comboBox_employees.currentIndex()
        empId = None
        if selectedEmpIdx > 0:
            #empModel = self.ui.comboBox_employees.model()
            #empId = empModel.data(empModel.index(selectedEmpIdx, 0)).toInt()[0]
            empId = self.getPKForCombobox(self.ui.comboBox_employees, 'din_id')
    
        query = """select din_id, din_nummer, din_name, dir_datum, dit_kbez, dit_beginn_ditid, dit_ende_ditid, dit_id, dir_id
                   from dienstnehmer_ereignisse, dir_typen, dienstnehmer 
                   where 1=1
                   and dir_ditid = dit_id 
                   and dir_dinid = din_id 
                   {empIdWhere}
                   order by din_name, dir_datum"""
                   
        query = query.format(empIdWhere=('' if empId is None else ' and din_id = %s '%(empId, )))
        
        return query
