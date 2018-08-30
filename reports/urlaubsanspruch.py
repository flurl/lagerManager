# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.urlaubsanspruchReport_gui import Ui_Urlaubsanspruch
from textReport import TextReport

import lib.Dienstnehmer

from lib.GlobalConfig import globalConf
from CONSTANTS import *



class UrlaubsanspruchReport(TextReport):

    uiClass = Ui_Urlaubsanspruch
    ident = 'urlaubsanspruch'

    def __init__(self, parent=None):
        TextReport.__init__(self, parent)

        self.setHeader('Urlaubsanspruch')
        self.setFooter('here could be a nice footer')
        #self.updateData()

    def setupUi(self):
        super(UrlaubsanspruchReport, self).setupUi()
        
        model = QtSql.QSqlTableModel()
        model.setTable('dienstnehmer')
        model.select()

        self.ui.comboBox_employees.setModel(model)
        self.ui.comboBox_employees.setModelColumn(model.fieldIndex('din_name'))

        self.ui.comboBox_employees.insertSeparator(-1)
        self.ui.comboBox_employees.setCurrentIndex(-1)


    def updateData(self):
        data = []
        dn = lib.Dienstnehmer.Dienstnehmer().find()
        while dn.next():
            print dn['din_name']
            ereignisse = dn['ereignisse']
            ereignisse.filter()
            avg = dn.getAvg('weekly', 104)
            data.append([dn['din_nummer'], dn['din_name'], avg[1], avg[2], avg[3], dn.getUsedVacationDays(), dn.getOpenVacationDays()])
        self.setData(data)
        self.process()
#    def setData(self, data):




    def setupSignals(self):
        super(UrlaubsanspruchReport, self).setupSignals()


    def setupUi(self):
        super(UrlaubsanspruchReport, self).setupUi()
