# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.dienstnehmerStatistikReport_gui import Ui_DienstnehmerStatistik
from textReport import TextReport

import lib.Dienstnehmer

from lib.GlobalConfig import globalConf
from CONSTANTS import *



class DienstnehmerStatistikReport(TextReport):

    uiClass = Ui_DienstnehmerStatistik
    ident = 'dienstnehmerStatistik'

    def __init__(self, parent=None):
        TextReport.__init__(self, parent)

        self.setHeader('Dienstnehmerstatistik')
        self.setFooter('here could be a nice footer')
        
        self.setTableHeaders()

        self.updateData()
        
        
    def setupUi(self):
        super(DienstnehmerStatistikReport, self).setupUi()

        model = QtSql.QSqlTableModel()
        model.setTable('dienstnehmer')
        model.select()

        self.ui.comboBox_employees.setModel(model)
        self.ui.comboBox_employees.setModelColumn(model.fieldIndex('din_name'))

        self.ui.comboBox_employees.insertSeparator(-1)
        self.ui.comboBox_employees.setCurrentIndex(-1)
        
        for i in range(1, 53):
            self.ui.comboBox_periodAmount.addItem(unicode(i))
        
    def setupSignals(self):
        super(DienstnehmerStatistikReport, self).setupSignals()
        self.connect(self.ui.comboBox_employees, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
        self.connect(self.ui.comboBox_calculationPeriod, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
        self.connect(self.ui.comboBox_periodAmount, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
        self.connect(self.ui.checkBox_singlePeriods, QtCore.SIGNAL('stateChanged(int)'), self.updateData)
        
    def setTableHeaders(self):
        if not self.ui.checkBox_singlePeriods.isChecked():
            headers = ['Nummer', 'Name', 'Durchrechnungsanzahl', 'Durch. Dienste', 'Durch. Stunden', 'Durch. NAZ']
        else:
            headers = ['Nummer', 'Name', 'Dienste', 'Stunden', 'NAZ', 'Jahr', 'Zeitraum']
        super(DienstnehmerStatistikReport, self).setTableHeaders(headers)
        
    def updateData(self):
        self.setTableHeaders()
        what = unicode(self.ui.comboBox_calculationPeriod.currentText()).lower()
        count = int(self.ui.comboBox_periodAmount.currentText())

        data = []

        selectedEmpIdx = self.ui.comboBox_employees.currentIndex()
        empId = None
        dn = lib.Dienstnehmer.Dienstnehmer()
        if selectedEmpIdx > 0:
            #empModel = self.ui.comboBox_employees.model()
            #empId = empModel.data(empModel.index(selectedEmpIdx, 0)).toInt()[0]
            empId = self.getPKForCombobox(self.ui.comboBox_employees, 'din_id')
            dn.get(empId)
        else:
            dn = dn.find()
            
#        print dn, empId, dn['din_name']
        while dn.next():
            if not self.ui.checkBox_singlePeriods.isChecked():
                data.append([dn['din_nummer'], dn['din_name']] + list(dn.getAvg(what, count)))
            else:
                dnData = dn.getTotals(what, count)
                for k, d in dnData.items():
                    print k, d
                    data.append([dn['din_nummer'], dn['din_name']] + list(d.values()) + list(k))
            
        self.setData(data)
        print(data)
        self.process()
