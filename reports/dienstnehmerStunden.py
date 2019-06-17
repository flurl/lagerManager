# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.dienstnehmerStundenReport_gui import Ui_DienstnehmerStunden
from textReport import TextReport

import lib.Dienst

from lib.GlobalConfig import globalConf
from CONSTANTS import *



class DienstnehmerStundenReport(TextReport):

    uiClass = Ui_DienstnehmerStunden
    ident = 'dienstnehmerStunden'

    def __init__(self, parent=None):
        self.tableHeaders = {
                            'single': ['Datum', 'Schicht', 'Name', 'DN-Nr.', 'Dienst Beginn', 'Dienst Ende', 'Anwesenheitsst.', 'Arbeitsstunden', 'Pause', 'Anzahl', 'Gehalt', 'NAZ', 'NAZ Anzahl', 'Feiertagsstunden', 'Trinkgeldp.', 'gesamt'],
                            'monthly': ['Monat', 'Name', 'DN-Nr.', 'Anwesenheitsst.', 'Arbeitsstunden', 'Pause', 'Anzahl', 'Gehalt', 'NAZ', 'NAZ Anzahl', 'Feiertagsstunden', 'Trinkgeldp.', 'gesamt'],
                            'yearly': ['Jahr', 'Name', 'DN-Nr.', 'Anwesenheitsst.', 'Arbeitsstunden', 'Pause', 'Anzahl', 'Gehalt', 'NAZ', 'NAZ Anzahl', 'Feiertagsstunden', 'Trinkgeldp.', 'gesamt']
                            }
        
        TextReport.__init__(self, parent)

        self.setHeader('Dienstnehmer Stunden Auswertung')
        self.setFooter('here could be a nice footer')
        
        self.setTableHeaders(self.tableHeaders['single'])

        #self.updateData()


    def updateData(self):
        data = []

        query =  self.mkQuery()
        results = self.db.exec_(query)
        while results.next():
            dieId = results.value(0).toInt()[0]
            d = lib.Dienst.Dienst(dieId)
            shift = d['schicht']
            emp = d['dienstnehmer']

            shiftName = shift['ver_bezeichnung']
            shiftDate = shift['ver_datum'].toPyDate()
            dutyBegin = d['die_beginn'].toPyDateTime()
            dutyEnd = d['die_ende'].toPyDateTime()
            empName = emp['din_name']
            empNr = emp['din_nummer']
            dutyHours = d.getTotalHours()
            workingHours = d.getWorkingHours()
            holidayHours = d.getFeiertagszuschlagStunden()
            dutyPause = d['die_pause']
            count = 1
            shiftSalary = d.getEarnings()
            shiftNAZ = d.getNAZ()
            NAZcount = 1 if shiftNAZ > 0.01 else 0
            tipAllowance = emp['beschaeftigungsbereich']['beb_trinkgeldpauschale']*workingHours*globalConf.getValueF('trinkgeldpauschale', d['die_beginn'])
            shiftSum = shiftSalary
            shiftSalary = shiftSalary - shiftNAZ - tipAllowance

            l = [shiftDate, shiftName, empName, empNr, dutyBegin, dutyEnd, dutyHours, workingHours, dutyPause, count, shiftSalary, shiftNAZ, NAZcount, holidayHours, tipAllowance, shiftSum]

            data.append(l)

        self.dataFromDb = data

        self.setData(data)
        self.process()

    def setData(self, data):

        if data is None:
            data = self.dataFromDb


        reportType = self.getReportType()

        dateFilter = self.ui.comboBox_timespan.itemData(self.ui.comboBox_timespan.currentIndex()).toInt()[0]
        if dateFilter > 0:
            if reportType == u'yearly':
                data = [row for row in data if row[0].year == dateFilter]
            else:
                data = [row for row in data if row[0].month == dateFilter]

        indexes = [idx.row() for idx in self.ui.listWidget_columns.selectedIndexes()]
        print "indexes: ", indexes
        
        data = self.groupBy(data, reportType)
        self.setTableHeaders([h for idx, h in enumerate(self.tableHeaders[reportType]) if idx in indexes])

        data.sort(key=lambda x: (x[0], x[1]))
        
        dataColumns = []
        for row in data:
            dataColumns.append([col for idx, col in enumerate(row) if idx in indexes])

        super(DienstnehmerStundenReport, self).setData(dataColumns)

        return True



    def setupSignals(self):
        super(DienstnehmerStundenReport, self).setupSignals()
        self.connect(self.ui.comboBox_reportType, QtCore.SIGNAL('currentIndexChanged(int)'), lambda: self.setupTimespanCombo() and self.setupColumnList() and self.setData(None) and self.process())
        self.connect(self.ui.pushButton_refresh, QtCore.SIGNAL('clicked()'), self.updateData)
        self.connect(self.ui.comboBox_employees, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
        self.connect(self.ui.comboBox_fieldOfEmployment, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateData)
        self.connect(self.ui.comboBox_timespan, QtCore.SIGNAL('currentIndexChanged(int)'),  lambda: self.setData(None) and self.process())
        self.connect(self.ui.listWidget_columns, QtCore.SIGNAL('itemClicked(QListWidgetItem *)'), lambda: self.setData(None) and self.process())


    def setupUi(self):
        super(DienstnehmerStundenReport, self).setupUi()

        model = QtSql.QSqlTableModel()
        model.setTable('dienstnehmer_view')
        model.select()

        sortModel = QtGui.QSortFilterProxyModel()
        sortModel.setDynamicSortFilter(True)
        sortModel.setSourceModel(model)
        sortModel.sort(model.fieldIndex('name'))

        self.ui.comboBox_employees.setModel(sortModel)
        self.ui.comboBox_employees.setModelColumn(model.fieldIndex('name'))

        self.ui.comboBox_employees.insertSeparator(-1)
        self.ui.comboBox_employees.setCurrentIndex(-1)

        model = QtSql.QSqlTableModel()
        model.setTable('beschaeftigungsbereiche')
        model.select()

        self.ui.comboBox_fieldOfEmployment.setModel(model)
        self.ui.comboBox_fieldOfEmployment.setModelColumn(model.fieldIndex('beb_bezeichnung'))

        self.ui.comboBox_fieldOfEmployment.insertSeparator(-1)
        self.ui.comboBox_fieldOfEmployment.setCurrentIndex(-1)

        self.setupTimespanCombo()
        self.setupColumnList()


    def setupTimespanCombo(self):
        combo = self.ui.comboBox_timespan
        combo.clear()

        reportType = unicode(self.ui.comboBox_reportType.currentText())

        if reportType == u'Jährlich':
            query = QtSql.QSqlQuery()
            query.prepare("select distinct YEAR(die_beginn) from dienste order by YEAR(die_beginn) DESC")
            query.exec_()
            while query.next():
                combo.addItem(query.value(0).toString(), query.value(0))

        else:
            for i in range(1,13):
                combo.addItem(unicode(i), i)

        combo.insertSeparator(-1)
        combo.setCurrentIndex(-1)

        return True

    def setupColumnList(self):
        print "setupColumnList"
        groupBy = self.getReportType()
        self.ui.listWidget_columns.clear()
        for col in self.tableHeaders[groupBy]:
            QtGui.QListWidgetItem(col, self.ui.listWidget_columns)
        self.ui.listWidget_columns.selectAll()
        
        return True
        
    def getReportType(self):
        reportType = unicode(self.ui.comboBox_reportType.currentText())
        if reportType == u'Monatlich':
            return 'monthly'
        elif reportType == u'Jährlich':
            return 'yearly'
        else:
            return 'single'


    def groupBy(self, data, groupBy='monthly'):
        if groupBy == 'single':
            return data

        newData = []
        emps = {}

        for row in data:
            if groupBy == 'monthly':
                group = (row[0].year, row[0].month)
            elif groupBy == 'yearly':
                group = (row[0].year, )

            if group not in emps:
                emps[group] = {}

            try:
                emp = emps[group][row[3]] #row[3] = DN-Nr., which should be unique
            except KeyError:
                emps[group][row[3]] = emp = {'name': row[2],
						                'number': row[3],
						                'totalHours': 0.0, 
						                'workingHours': 0.0, 
						                'pause': 0.0, 
						                'count': 0.0, 
						                'salary': 0.0,
						                'NAZ': 0.0,
						                'NAZcount': 0,
						                'holidayHours': 0,
						                'tipAllowance': 0.0,
						                'sum': 0.0
						                }

            emp['totalHours'] += row[6]
            emp['workingHours'] += row[7]
            emp['pause'] += row[8]
            emp['count'] += row[9]
            emp['salary'] += row[10]
            emp['NAZ'] += row[11]
            emp['NAZcount'] += row[12]
            emp['holidayHours'] += row[13]
            emp['tipAllowance'] += row[14]
            emp['sum'] += row[15]

        for group in emps:
            for emp in emps[group]:
                e = emps[group][emp]
                newData.append([u'-'.join([unicode(x) for x in group]), e['name'], e['number'], e['totalHours'], e['workingHours'], e['pause'], e['count'], e['salary'], e['NAZ'], e['NAZcount'], e['holidayHours'], e['tipAllowance'], e['sum']])

        return newData


    def mkQuery(self):
        """return the query"""
        reportType = unicode(self.ui.comboBox_reportType.currentText())
        pStart, pEnd = self._getCurrentPeriodStartEnd()

        selectedEmpIdx = self.ui.comboBox_employees.currentIndex()
        empId = None
        if selectedEmpIdx > 0:
            empModel = self.ui.comboBox_employees.model()
            empId = empModel.data(empModel.index(selectedEmpIdx, 0)).toInt()[0]

        selectedFOEIdx = self.ui.comboBox_fieldOfEmployment.currentIndex()
        foeId = None
        if selectedFOEIdx > 0:
            foeModel = self.ui.comboBox_fieldOfEmployment.model()
            foeId = foeModel.data(foeModel.index(selectedFOEIdx, 0)).toInt()[0]


        query = """
                select {fields}
                from dienstnehmer, dienste, veranstaltungen, beschaeftigungsbereiche
                where 1=1
                and die_dinid = din_id
                and die_verid = ver_id
                and din_bebid = beb_id
                {empIdWhere}
                {foeIdWhere}
                and ver_datum between '{pStart}' and '{pEnd}'
                order by ver_datum desc
                """

        fields = 'die_id'

        query = query.format(
			                fields=fields,
			                pStart=pStart.strftime('%Y-%m-%d %H:%M:%S'), 
			                pEnd=pEnd.strftime('%Y-%m-%d %H:%M:%S'),
			                empIdWhere=("" if empId is None else " and din_id = %s "%(empId, )),
			                foeIdWhere=("" if foeId is None else " and beb_id = %s "%(foeId, ))
			                )

        return query

