# -*- coding: utf-8 -*-
from __future__ import print_function

import numbers
from sets import Set
import sip

from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import MINHOURSFORPAUSE
from forms.formBase import FormBase, ComboBoxPKError
import lib.Arbeitsplatz
from lib.Beschaeftigungsbereich import Beschaeftigungsbereich
import lib.Dienst
import lib.Dienstnehmer
from lib.GlobalConfig import globalConf
import lib.Schicht
from ui.forms.dienstplanForm_gui import Ui_DienstplanForm


class DienstplanForm(FormBase):
    
    uiClass = Ui_DienstplanForm
    ident = 'dienstplan'
    
    def __init__(self, parent):
        self.employees = []
        self.modified = False
        self.__drawTimer = QtCore.QTimer()
        self.__loading = False
        super(DienstplanForm, self).__init__(parent)
        self.load()
        
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowSystemMenuHint
                            | QtCore.Qt.WindowMinimizeButtonHint
                            | QtCore.Qt.WindowMaximizeButtonHint
                            | QtCore.Qt.WindowCloseButtonHint)
    
    def setupUi(self):
        super(DienstplanForm, self).setupUi()
        eventsModel = QtSql.QSqlTableModel()
        eventsModel.setTable('veranstaltungen')
        eventsModel.setSort(eventsModel.fieldIndex('ver_datum'),
                            QtCore.Qt.DescendingOrder)
        eventsModel.select()
        
        view = QtGui.QTableView()
        view.setModel(eventsModel)

        # Do with the view whatever you like
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        view.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        view.setAutoScroll(False)
        view.resizeColumnsToContents()
        view.resizeRowsToContents()
        # view.setSortingEnabled(True)
        view.verticalHeader().setVisible(False)  # Rownumbers
        view.setMinimumWidth(view.horizontalHeader().length())
        view.setColumnHidden(0, True)
        view.setColumnHidden(4, True)

        # The important part: First set the model, then the view on the box
        # box.setModel(model)
        # box.setView(view)
        
        self.ui.comboBox_event.setModel(eventsModel)
        self.ui.comboBox_event.setView(view)
        self.ui.comboBox_event.setModelColumn(eventsModel.
                                              fieldIndex('ver_bezeichnung'))
        
        templateModel = QtSql.QSqlQueryModel()
        templateModel.setQuery('select distinct div_bezeichnung \
                                from dienste_vorlagen')
        self.ui.comboBox_template.setModel(templateModel)
        # self.ui.comboBox_template.setModelColumn(1)
        
    def setupSignals(self):
        super(DienstplanForm, self).setupSignals()
        self.connect(self.ui.pushButton_addEmployee,
                     QtCore.SIGNAL('clicked()'),
                     lambda: self.setModified(True) and self.addEmployee())
        self.connect(self.ui.pushButton_sort,
                     QtCore.SIGNAL('clicked()'),
                     self.sortWidgets)
        self.connect(self.ui.buttonBox,
                     QtCore.SIGNAL('accepted()'),
                     self.accept)
        self.connect(self.ui.buttonBox,
                     QtCore.SIGNAL('rejected()'),
                     self.reject)
        self.connect(self.ui.buttonBox,
                     QtCore.SIGNAL('clicked(QAbstractButton *)'),
                     self.onButtonBoxClicked)
        self.connect(self.ui.comboBox_event,
                     QtCore.SIGNAL('currentIndexChanged(int)'),
                     self.load)
        self.connect(self.ui.pushButton_saveTemplate,
                     QtCore.SIGNAL('clicked()'),
                     self.saveTemplate)
        self.connect(self.ui.pushButton_loadTemplate,
                     QtCore.SIGNAL('clicked()'),
                     self.loadTemplate)
        self.connect(self.ui.pushButton_autoAssignEmps,
                     QtCore.SIGNAL('clicked()'),
                     self.autoAssignEmployees)
        #always scroll to bottom
        sBar = self.ui.scrollArea.verticalScrollBar()
        self.connect(sBar,
                     QtCore.SIGNAL('rangeChanged(int,int)'),
                     lambda min_, max_, scroll=sBar: scroll.setValue(max_))
        
    def addEmployee(self, dinId=None, arpId=None, dieBeginn=None,
                    dieEnde=None, diePause=None):
        eventProps = self.getEventProperties(self.getCurrentEventId())
        layout = QtGui.QVBoxLayout()
        workLayout = QtGui.QHBoxLayout()
        
        workplaceModel = QtSql.QSqlTableModel()
        workplaceModel.setTable('arbeitsplaetze')
        workplaceModel.select()
        workplaceCombo = QtGui.QComboBox()
        workplaceCombo.setModel(workplaceModel)
        workplaceCombo.setModelColumn(workplaceModel.
                                      fieldIndex('arp_bezeichnung'))
        workLayout.addWidget(workplaceCombo)
        
        employeeModel = QtSql.QSqlTableModel()
        employeeModel.setTable('dienstnehmer_view')
        employeeModel.select()
        employeeCombo = QtGui.QComboBox()
        employeeCombo.setModel(employeeModel)
        employeeCombo.setModelColumn(employeeModel.fieldIndex(u'name'))
        workLayout.addWidget(employeeCombo)
        
        dutyCountLineEdit = QtGui.QLineEdit()
        dutyCountLineEdit.setReadOnly(True)
        dutyCountLineEdit.setFixedWidth(50)
        workLayout.addWidget(dutyCountLineEdit)
        
        layout.addLayout(workLayout)
        
        beginDateTimeEdit = QtGui.QDateTimeEdit()
        beginDateTimeEdit.setCalendarPopup(True)
        # events starting after midnight might need shift starts on the day before
        if 0 <= eventProps['ver_beginn'].hour() <= 6:
            beginDateTimeEdit.setMinimumDate(eventProps['ver_datum'].addDays(-1))
        else:
            beginDateTimeEdit.setMinimumDate(eventProps['ver_datum'])
        beginDateTimeEdit.setMaximumDate(eventProps['ver_datum'].addDays(1))
        
        endDateTimeEdit = QtGui.QDateTimeEdit()
        endDateTimeEdit.setCalendarPopup(True)
        endDateTimeEdit.setMinimumDate(eventProps['ver_datum'])
        endDateTimeEdit.setMaximumDate(eventProps['ver_datum'].addDays(1))
        
        shiftLengthLineEdit = QtGui.QLineEdit()
        shiftLengthLineEdit.setReadOnly(True)
        shiftLengthLineEdit.setFixedWidth(50)
        
        pauseCheckBox = QtGui.QCheckBox()
        pauseCheckBox.setText(u'Pause')
        pauseCheckBox.setEnabled(False)
        
        NAZCheckBox = QtGui.QCheckBox()
        NAZCheckBox.setText(u'NAZ')
        NAZCheckBox.setEnabled(False)
        
        timeLayout = QtGui.QHBoxLayout()
        timeLayout.addWidget(beginDateTimeEdit)
        timeLayout.addWidget(endDateTimeEdit)
        timeLayout.addWidget(shiftLengthLineEdit)
        timeLayout.addWidget(pauseCheckBox)
        timeLayout.addWidget(NAZCheckBox)
        layout.addLayout(timeLayout)
        
        delBtn = QtGui.QPushButton(u'löschen')
        layout.addWidget(delBtn)
        
        frame = QtGui.QFrame()
        frame.setFrameShape(QtGui.QFrame.Box)
        # frame.setFrameShadow(QtGui.QFrame.Sunken)
        frame.setLayout(layout)
        frame.showEvent = lambda e, f = frame: self.onFrameShown(f, e)
        # insert before the push button; -2 because there are already
        # 2 widget in the layout: the button and the spacer
        (self.ui.verticalLayout_employees.
         insertWidget(self.ui.verticalLayout_employees.count() - 2, frame))
        
        widgetRef = {'workplaceCombo': workplaceCombo,
                     'employeeCombo': employeeCombo,
                     'dutyCountLineEdit': dutyCountLineEdit,
                     'beginDateTimeEdit': beginDateTimeEdit,
                     'endDateTimeEdit': endDateTimeEdit,
                     'shiftLengthLineEdit': shiftLengthLineEdit,
                     'pauseCheckBox': pauseCheckBox,
                     'frame': frame,
                     'NAZCheckBox': NAZCheckBox
                    }
        
        if arpId is not None:
            idx = workplaceModel.match(workplaceModel.index(0, 0), 0, arpId)[0]
            workplaceCombo.setCurrentIndex(idx.row())
        else:
            workplaceCombo.insertSeparator(-1)
            workplaceCombo.setCurrentIndex(-1)
            employeeCombo.setEnabled(False)
            
        self.checkEmployeeWorkplaceAssignment(widgetRef)
            
        if dinId is not None:
            idx = employeeModel.match(employeeModel.index(0, 0), 0, dinId)[0]
            employeeCombo.setCurrentIndex(idx.row())
            self.getEmployeeDutyCount(widgetRef)
        else:
            employeeCombo.insertSeparator(-1)
            employeeCombo.setCurrentIndex(-1)
            
        if dieBeginn is not None and isinstance(dieBeginn, QtCore.QDateTime):
            beginDateTimeEdit.setDateTime(dieBeginn)
        elif dieBeginn is not None and isinstance(dieBeginn, QtCore.QTime):
            beginDateTimeEdit.setDate(eventProps['ver_datum'])
            beginDateTimeEdit.setTime(dieBeginn)
        else:
            beginDateTimeEdit.setDate(eventProps['ver_datum'])
            beginDateTimeEdit.setTime(eventProps['ver_beginn'])
            
        if dieEnde is not None and isinstance(dieEnde, QtCore.QDateTime):
            endDateTimeEdit.setDateTime(dieEnde)
        elif dieEnde is not None and isinstance(dieEnde, QtCore.QTime):
            endDateTimeEdit.setDate(eventProps['ver_datum'].addDays(1))
            endDateTimeEdit.setTime(dieEnde)
        elif dieEnde is not None and isinstance(dieEnde, numbers.Number):
            endDateTimeEdit.setDateTime(beginDateTimeEdit.dateTime().addSecs(dieEnde))
        else:
            try:
                workplace = lib.Arbeitsplatz.Arbeitsplatz(self.
                                                      getPKForCombobox(workplaceCombo, 'arp_id'))
                endDateTimeEdit.setDate(eventProps['ver_datum'])
                endDateTimeEdit.setTime(eventProps['ver_beginn'])
                endDateTimeEdit.setDateTime(endDateTimeEdit.dateTime().
                                            addSecs(int(workplace['arp_std_dienst_dauer'] * 3600)))
            except ComboBoxPKError:
                endDateTimeEdit.setDateTime(QtCore.QDateTime())
        
        # set the seconds of the datetimeedit to 0
        edit = beginDateTimeEdit
        editTime = edit.time()
        editTime.setHMS(editTime.hour(), editTime.minute(), 0)
        edit.setTime(editTime)
        
        edit = endDateTimeEdit
        editTime = edit.time()
        editTime.setHMS(editTime.hour(), editTime.minute(), 0)
        edit.setTime(editTime)
            
        if diePause is not None and diePause > 0.001:
            pauseCheckBox.setChecked(QtCore.Qt.Checked)
        
        self.setEmployeeFrameColor(widgetRef)
        
        self.connect(workplaceCombo,
                     QtCore.SIGNAL('currentIndexChanged(int)'),
                     lambda: self.setModified(True))
        self.connect(employeeCombo,
                     QtCore.SIGNAL('currentIndexChanged(int)'),
                     lambda: self.setModified(True))
        self.connect(beginDateTimeEdit,
                     QtCore.SIGNAL('dateTimeChanged (const QDateTime&)'),
                     lambda: self.setModified(True))
        self.connect(endDateTimeEdit,
                     QtCore.SIGNAL('dateTimeChanged (const QDateTime&)'),
                     lambda: self.setModified(True))
        self.connect(pauseCheckBox,
                     QtCore.SIGNAL('stateChanged(int)'),
                     lambda: self.setModified(True))
        
        self.connect(delBtn,
                     QtCore.SIGNAL('clicked()'),
                     lambda: self.setModified(True))
        self.connect(delBtn,
                     QtCore.SIGNAL('clicked()'),
                     (lambda f=frame, wr=widgetRef:
                      self.deleteWidget(f) and self.employees.remove(wr)))
        
        self.connect(employeeCombo,
                     QtCore.SIGNAL('currentIndexChanged(int)'),
                     lambda i, wr=widgetRef: self.checkEmployeeHours(wr))
        self.connect(beginDateTimeEdit,
                     QtCore.SIGNAL('dateTimeChanged (const QDateTime&)'),
                     lambda dt, wr=widgetRef: self.checkEmployeeHours(wr))
        self.connect(endDateTimeEdit,
                     QtCore.SIGNAL('dateTimeChanged (const QDateTime&)'),
                     lambda dt, wr=widgetRef: self.checkEmployeeHours(wr))
        self.connect(pauseCheckBox,
                     QtCore.SIGNAL('stateChanged(int)'),
                     lambda i, wr=widgetRef: self.checkEmployeeHours(wr))
        
        self.connect(beginDateTimeEdit,
                     QtCore.SIGNAL('dateTimeChanged (const QDateTime&)'),
                     lambda dt, wr=widgetRef: self.checkDateTime(wr))
        self.connect(endDateTimeEdit,
                     QtCore.SIGNAL('dateTimeChanged (const QDateTime&)'),
                     lambda dt, wr=widgetRef: self.checkDateTime(wr))
        
        self.connect(employeeCombo,
                     QtCore.SIGNAL('currentIndexChanged(int)'),
                     lambda i, wr=widgetRef: self.setEmployeeFrameColor(wr))
        self.connect(workplaceCombo,
                     QtCore.SIGNAL('currentIndexChanged(int)'),
                     lambda i, wr=widgetRef: self.checkEmployeeWorkplaceAssignment(wr))
        
        self.employees.append(widgetRef)
        self.checkDateTime(widgetRef)
        
        return widgetRef
    
    def sortWidgets(self):
        l = self.ui.verticalLayout_employees
        for wr in self.employees:
            self.ui.verticalLayout_employees.removeWidget(wr['frame'])
        
        foeIds = []
        for wr in self.employees:
            try:
                foeId = self.getWorkplaceProperties(self.
                                                   getPKForCombobox(wr['workplaceCombo'],
                                                                    'arp_id'))['arp_bebid']
            except ComboBoxPKError:
                foeId = 0
                
            if not foeIds:
                l.insertWidget(0, wr['frame'])
                foeIds = [foeId]
                continue
            
            for i in reversed(range(len(foeIds))):
                if foeIds[i] < foeId:
                    i += 1
                    break
            
            l.insertWidget(i, wr['frame'])
            foeIds.insert(i, foeId)
        
        self.drawTimeTable()
    
    def findEmployeeWidgetRefByEmpId(self, empId):
        for emp in self.employees:
            id_ = self.getPKForCombobox(emp['employeeCombo'], 'din_id')
            if id_ == empId:
                return emp
    
    def setModified(self, state=True):
        self.drawTimeTable()
        # don't modify state while loading
        if not self.__loading:
            self.modified = state
        return True
    
    def validateRoster(self):
        
        def get_duplicate_items(L):
            new = Set()
            for item in L:
                if L.count(item) > 1:
                    new.add(item)
            return list(new)
        
        print("validateRoster")
        employeesInUse = []
        for waiterWidgetRefs in self.employees:
            try:
                empId = self.getPKForCombobox(waiterWidgetRefs['employeeCombo'], 'din_id')
            except ComboBoxPKError:
                QtGui.QMessageBox.warning(self, u'Einteilungsfehler',
                                                u'Ein oder mehreren Diensten \
                                                wurde kein DN zugewiesen')
                return False
            employeesInUse.append(empId)
            
            try:
                self.getPKForCombobox(waiterWidgetRefs['workplaceCombo'], 'arp_id')
            except ComboBoxPKError:
                QtGui.QMessageBox.warning(self, u'Einteilungsfehler',
                                                u'Ein oder mehreren Diensten \
                                                wurde kein Arbeitsplatz zugewiesen')
                return False
            
            failedTimes = self.checkDateTime(waiterWidgetRefs)
            if failedTimes:
                QtGui.QMessageBox.warning(self, u'Zeiten Fehler',
                                                u'Beginn und Ende des Dienstes liegen vor \
                                                Schichtbeginn! Arbeitsplatz: %s' % failedTimes)
                return False
            
        duplicateWaiters = get_duplicate_items(employeesInUse)
        if len(duplicateWaiters):
            QtGui.QMessageBox.warning(self, u'Doppelte Einteilung',
                                            u'Der/die Kellner %s wurde doppelt \
                                            eingeteilt' % duplicateWaiters)
            return False
        
        failingEmployees = self.checkMonthlyWorkingHours(employeesInUse)
        if len(failingEmployees) > 0:
            QtGui.QMessageBox.warning(self, u'Arbeitszeitüberschreitung',
                                            u'Folgende Dienstnehmer überschreiten ihre \
                                            monatliche Arbeitszeit: %s' % failingEmployees)
            return False
        
        unavailableEmployees = self.checkEmployeeAvailability(employeesInUse)
        if unavailableEmployees is False or len(unavailableEmployees) > 0:
            QtGui.QMessageBox.warning(self, u'Doppelte Einteilung',
                                            u'Folgende Dienstnehmer sind bereits in einer \
                                            anderen Schicht eingeteilt: %s' % unavailableEmployees)
            return False
        
        return True
    
    def checkMonthlyWorkingHours(self, empIds):
        print("checkMonthlyWorkingHours")
        eventProps = self.getEventProperties(self.getCurrentEventId())
        eventDate = eventProps['ver_datum']
        failingEmployees = []
                
        for empId in empIds:
            widgetRef = self.findEmployeeWidgetRefByEmpId(empId)
            beginDate = widgetRef['beginDateTimeEdit'].dateTime()
            endDate = widgetRef['endDateTimeEdit'].dateTime()
            
            emp = lib.Dienstnehmer.Dienstnehmer(empId)
            print('shift:', eventDate, eventProps['ver_id'])
            remainingSalary = emp.getRemainingSalary(eventDate.toPyDate(), eventProps['ver_id'])
            duty = lib.Dienst.Dienst()
            duty['die_beginn'] = beginDate
            duty['die_ende'] = endDate
            duty['die_dinid'] = empId
            
            dutyEarnings = duty.getEarnings()
            
            print('checkMonthlyWorkingHours remainingSalary:',
                  remainingSalary, 'dutyEarnings:', dutyEarnings)
            
            if dutyEarnings > remainingSalary:
                failingEmployees.append((emp['din_id'], emp['din_name'],
                                         'Verbleibendes Gehalt: %s, benötigt: %s'
                                         % (remainingSalary, dutyEarnings)))
            
        return failingEmployees
    
    def checkEmployeeHours(self, widgetRef):
        print("checkEmployeeHours")
        combo = widgetRef['employeeCombo']
        try:
            empId = self.getPKForCombobox(combo, 'din_id')
        except ComboBoxPKError:
            return
        failed = self.checkMonthlyWorkingHours([empId])
        if len(failed) > 0:
            combo.setStyleSheet('QFrame {background-color:red;}')
        else:
            combo.setStyleSheet('')
        self.getEmployeeDutyCount(widgetRef)
        
        
    def getEmployeeDutyCount(self, widgetRef):
        combo = widgetRef['employeeCombo']
        try:
            empId = self.getPKForCombobox(combo, 'din_id')
        except ComboBoxPKError:
            return
        emp = lib.Dienstnehmer.Dienstnehmer(empId)
        eventProps = self.getEventProperties(self.getCurrentEventId())
        eventDate = eventProps['ver_datum'].toPyDate()
        dutyCount = len(emp.getDuties(eventDate))
        widgetRef['dutyCountLineEdit'].setText(unicode(dutyCount))
        

    def checkDateTime(self, wr):
        begin = wr['beginDateTimeEdit'].dateTime()
        end = wr['endDateTimeEdit'].dateTime()
        try:
            empId = self.getPKForCombobox(wr['employeeCombo'], 'din_id')
        except ComboBoxPKError:
            return False
        
        modified = False
        if end <= begin:
            wpId = self.getPKForCombobox(wr['workplaceCombo'], 'arp_id')
            wpProps = self.getWorkplaceProperties(wpId)
            wr['endDateTimeEdit'].setDateTime(begin.
                                              addSecs(int(wpProps['arp_std_dienst_dauer'] * 3600)))
            end = wr['endDateTimeEdit'].dateTime()
            modified = True
            QtGui.QMessageBox.warning(self, u'Zeiten Fehler',
                                            u'Das End-Datum liegt vor dem Beginn-Datum! \
                                            Zeitraum wurde angepasst.')
        
        duty = lib.Dienst.Dienst()
        duty['die_beginn'] = begin
        duty['die_ende'] = end
        duty['die_dinid'] = empId
        
        hours = duty.getWorkingHours()
        pause = duty.getPauseHours()
        NAZ = duty.getNAZ()
        
        if pause > 0.01:
            if not wr['pauseCheckBox'].isChecked():
                wr['pauseCheckBox'].setChecked(True)
                modified = True
        else:
            if wr['pauseCheckBox'].isChecked():
                wr['pauseCheckBox'].setChecked(False)
                modified = True
        
        wr['shiftLengthLineEdit'].setText(unicode(hours))
        
        cb = wr['NAZCheckBox']
        if NAZ > 0:
            if not cb.isChecked():
                cb.setChecked(True)
                modified = True
        else:
            if cb.isChecked():
                cb.setChecked(False)
                modified = True
        
        if modified:
            self.setModified()
            
        shiftProps = self.getEventProperties(self.getCurrentEventId())
        if begin < shiftProps['date_time'] and end < shiftProps['date_time']:
            return [(wr['workplaceCombo'].currentText(), wr['employeeCombo'].currentText())]
    
    def checkEmployeeAvailability(self, empIds):
        print("checkEmployeeAvailability")
        failingEmployees = []
        for empId in empIds:
            widgetRef = self.findEmployeeWidgetRefByEmpId(empId)
            beginDate = widgetRef['beginDateTimeEdit'].dateTime()
            endDate = widgetRef['endDateTimeEdit'].dateTime()
            
            query = QtSql.QSqlQuery()
            query.prepare('select count(*) from dienste \
                           where die_dinid = ? and die_verid != ? \
                           and (die_beginn between ? and ? or die_ende between ? and ?)')
            query.addBindValue(empId)
            query.addBindValue(self.getCurrentEventId())
            query.addBindValue(beginDate)
            query.addBindValue(endDate)
            query.addBindValue(beginDate)
            query.addBindValue(endDate)
            
            query.exec_()
            
            if query.lastError().isValid():
                print('Error while selecting dienste for employee %s:'
                      % empId, query.lastError().text())
                QtGui.QMessageBox.warning(self, u'Datenbank Fehler',
                                                u'Fehler beim abrufen der Dienste!\n\
                                                Bitte kontaktieren Sie Ihren Administrator.')
                return False
            
            query.next()
            
            count = query.value(0).toInt()[0]

            if count != 0 or not lib.Dienstnehmer.Dienstnehmer(empId).isAvailableForDate(beginDate):
                empProps = self.getEmployeeProperties(empId)
                failingEmployees.append((empProps['din_id'], empProps['din_name']))
            
        return failingEmployees
    
    
    
    def checkEmployeeWorkplaceAssignment(self, wr):
        try:
            pk = self.getPKForCombobox(wr['workplaceCombo'], 'arp_id')
        except ComboBoxPKError:
            return
    
        wpProps = self.getWorkplaceProperties(pk)
        eventProps = self.getEventProperties(self.getCurrentEventId())
        combo = wr['employeeCombo']
        # if the combo is not enabled, no workplace has been selected until now
        # this means we init the end datetime the first time
        if not combo.isEnabled():
            combo.setEnabled(True)
            edit = wr['endDateTimeEdit']
            edit.setDate(eventProps['ver_datum'])
            edit.setTime(eventProps['ver_beginn'])
            edit.setDateTime(edit.dateTime().addSecs(int(wpProps['arp_std_dienst_dauer'] * 3600)))
        combo.model().setFilter("dienstnehmer_view.din_bebid = %s and empIsAvailableForDate(din_id, '%s') = 1" %
                                              (wpProps['arp_bebid'], eventProps['ver_datum'].toPyDate().isoformat()))
    
    def setEmployeeFrameColor(self, wr):
        try:
            empProps = self.getEmployeeProperties(self.getPKForCombobox(wr['employeeCombo'],
                                                                        'din_id'))
        except ComboBoxPKError:
            return
        color = empProps['din_farbe']
        print('color:', empProps['din_farbe'], 'background-color:%s;' % color)
        wr['frame'].setStyleSheet('QFrame {background-color:%s;} \
                                   QComboBox QAbstractItemView {background: transparent;} \
                                   QCheckBox {background: white;}' % color)
        
    def accept(self):
        if not self.modified or self.save():
            super(DienstplanForm, self).accept()
        
    def save(self):
        if not self.validateRoster():
            return False
        
        try:
            self.beginTransaction()
            eventId = self.getPKForCombobox(self.ui.comboBox_event, 'ver_id')
            
            query = QtSql.QSqlQuery()
            query.prepare("delete from dienste where die_verid = ?")
            query.addBindValue(eventId)
            query.exec_()
            if query.lastError().isValid():
                self.rollback()
                print('Error while deleting dienstplan for event:', query.lastError().text())
                QtGui.QMessageBox.warning(self, u'Datenbank Fehler',
                                                u'Fehler beim Speichern des Dienstplans!\n\
                                                Bitte kontaktieren Sie Ihren Administrator.')
                return False
            
            for waiterWidgetRefs in self.employees:
                empId = self.getPKForCombobox(waiterWidgetRefs['employeeCombo'], 'din_id')
                wpId = self.getPKForCombobox(waiterWidgetRefs['workplaceCombo'], 'arp_id')
                begin = waiterWidgetRefs['beginDateTimeEdit'].dateTime()
                end = waiterWidgetRefs['endDateTimeEdit'].dateTime()
                pause = 0.5 if waiterWidgetRefs['pauseCheckBox'].isChecked() else 0.0
                
                query = QtSql.QSqlQuery()
                query.prepare("""
                                insert into dienste (die_dinid, die_verid,
                                die_arpid, die_beginn, die_ende, die_pause)
                                values (?, ?, ?, ?, ?, ?)
                                """)
                query.addBindValue(empId)
                query.addBindValue(eventId)
                query.addBindValue(wpId)
                query.addBindValue(begin)
                query.addBindValue(end)
                query.addBindValue(pause)
                query.exec_()
                if query.lastError().isValid():
                    self.rollback()
                    print('Error while inserting dienstplan:', query.lastError().text())
                    QtGui.QMessageBox.warning(self, u'Datenbank Fehler',
                                                    u'Fehler beim Speichern des Dienstplans!\n\
                                                    Bitte kontaktieren Sie Ihren Administrator.')
                    return False
                
            self.commit()
        except Exception as e:
            print("exception in save()", e)
            self.rollback()
        
        self.setModified(False)
        return True
            
    def load(self):
        if not self.askToContinueIfModified():
            cb = self.ui.comboBox_event
            oldState = cb.blockSignals(True)
            cb.setCurrentIndex(cb.previousIndex())
            cb.blockSignals(oldState)
            return False
        
        self.__loading = True
        
        self.clear()
        
        self.setModified(False)
        
        eventId = self.getCurrentEventId()
        print("event:", eventId)
        query = QtSql.QSqlQuery()
        query.prepare("select die_id, die_dinid, die_arpid, die_beginn, die_ende, die_pause \
                       from dienste where die_verid = ?")
        query.addBindValue(eventId)
        query.exec_()
        if query.lastError().isValid():
            print('Error while selecting dienstplan:', query.lastError().text())
            QtGui.QMessageBox.warning(self, u'Datenbank Fehler',
                                            u'Fehler beim Laden des Dienstplans!\n\
                                            Bitte kontaktieren Sie Ihren Administrator.')
            return False
        
        while query.next():
            dinId = query.value(1).toInt()[0]
            arpId = query.value(2).toInt()[0]
            dieBeginn = query.value(3).toDateTime()
            dieEnde = query.value(4).toDateTime()
            diePause = query.value(5).toFloat()[0]
            
            self.addEmployee(dinId, arpId, dieBeginn, dieEnde, diePause)
        
        self.__loading = False
        self.sortWidgets()
        
    def onButtonBoxClicked(self, btn):
        if self.ui.buttonBox.buttonRole(btn) == QtGui.QDialogButtonBox.ApplyRole:
            if self.modified:
                if self.save():
                    QtGui.QMessageBox.information(self, u'Speichern erfolgreich',
                                                u'Änderungen erfolgreich gespeichert.')
    
    def deleteWidget(self, w):
        self.ui.verticalLayout_employees.removeWidget(w)
        sip.delete(w)
        w = None
        return True
        
    def clear(self):
        layout = self.ui.verticalLayout_employees
        while layout.count() > 2:
            child = layout.takeAt(0)
            w = child.widget()
            if w:
                self.deleteWidget(w)
        self.employees = []
        return True
    
    def saveTemplate(self):
        name, ok = QtGui.QInputDialog.getText(
                                              self, u'Vorlagenname',
                                              u'Bitte gib einen Namen für die Vorlage ein',
                                              QtGui.QLineEdit.Normal,
                                              self.ui.comboBox_template.currentText())
        if ok:
            query = QtSql.QSqlQuery()
            query.prepare('select count(*) from dienste_vorlagen where div_bezeichnung = ?')
            query.addBindValue(name)
            query.exec_()
            if query.lastError().isValid():
                print('Error while selecting dienste_vorlagen:', query.lastError().text())
                QtGui.QMessageBox.warning(self, u'Datenbank Fehler',
                                                u'Fehler beim Selektieren der Dienstvorlagen!\n\
                                                Bitte kontaktieren Sie Ihren Administrator.')
                return False
            query.next()
            count = query.value(0).toInt()[0]
            
            if count > 0:
                answer = QtGui.QMessageBox.question(self, u'Vorlage existiert',
                                                    u'Die Vorlage %s wird überschrieben. \
                                                    Sind Sie sicher?.' % unicode(name),
                                                    QtGui.QMessageBox.Yes,
                                                    QtGui.QMessageBox.No)
                if answer == QtGui.QMessageBox.No:
                    return False
            
            try:
                self.beginTransaction()
                
                query = QtSql.QSqlQuery()
                query.prepare('delete from dienste_vorlagen where div_bezeichnung = ?')
                query.addBindValue(name)
                query.exec_()
                if query.lastError().isValid():
                    print('Error while deleting dienste_vorlagen:', query.lastError().text())
                    QtGui.QMessageBox.warning(self, u'Datenbank Fehler',
                                                    u'Fehler beim Löschen der Dienstvorlagen!\n\
                                                    Bitte kontaktieren Sie Ihren Administrator.')
                    raise Exception()
                
                for waiterWidgetRefs in self.employees:
                    wpId = self.getPKForCombobox(waiterWidgetRefs['workplaceCombo'], 'arp_id')
                    begin = waiterWidgetRefs['beginDateTimeEdit'].time()
                    duration = (waiterWidgetRefs['beginDateTimeEdit'].
                                dateTime().secsTo(waiterWidgetRefs['endDateTimeEdit'].
                                                  dateTime()))
                    
                    query = QtSql.QSqlQuery()
                    query.prepare("""
                                    insert into dienste_vorlagen \
                                    (div_bezeichnung, div_arpid, div_beginn, div_dauer)
                                    values (?, ?, ?, ?)
                                    """)
                    query.addBindValue(name)
                    query.addBindValue(wpId)
                    query.addBindValue(begin)
                    query.addBindValue(duration)
                    query.exec_()
                    if query.lastError().isValid():
                        print('Error while inserting dienstplan template:',
                              query.lastError().text())
                        QtGui.QMessageBox.warning(self,
                                                  u'Datenbank Fehler',
                                                  u'Fehler beim Speichern der Dienstplan Vorlage!\
                                                  \nBitte kontaktieren Sie Ihren Administrator.')
                        raise Exception()
            
            except Exception as e:
                self.rollback()
                print(e)
                return False
            else:
                self.commit()
            
            self.ui.comboBox_template.model().query().exec_()
            self.ui.comboBox_template.model().setQuery(self.ui.comboBox_template.model().query())
            return True
        
    def loadTemplate(self):
        if not self.askToContinueIfModified():
            return False
        
        self.clear()
        
        tmplName = self.ui.comboBox_template.currentText()
        query = QtSql.QSqlQuery()
        query.prepare('select div_id, div_bezeichnung, div_arpid, div_beginn, div_dauer \
                       from dienste_vorlagen where div_bezeichnung = ?')
        query.addBindValue(tmplName)
        query.exec_()
        if query.lastError().isValid():
            print('Error while getting dienstplan template:', query.lastError().text())
            QtGui.QMessageBox.warning(self, u'Datenbank Fehler',
                                            u'Fehler beim Laden der Dienstplan Vorlage!\n\
                                            Bitte kontaktieren Sie Ihren Administrator.')
        while query.next():
            wpId = query.value(2).toInt()[0]
            begin = query.value(3).toTime()
            duration = query.value(4).toInt()[0]
            self.addEmployee(arpId=wpId, dieBeginn=begin, dieEnde=duration)
            # self.checkDateTime(wr)
        
        self.autoAssignEmployees()
        self.setModified()
        self.sortWidgets()
        
    def autoAssignEmployees(self):
        alreadyAssignedEmps = []
        
        for waiterWidgetRefs in self.employees:
            wpId = self.getPKForCombobox(waiterWidgetRefs['workplaceCombo'], 'arp_id')
            begin = waiterWidgetRefs['beginDateTimeEdit'].dateTime()
            end = waiterWidgetRefs['endDateTimeEdit'].dateTime()
            
            query = QtSql.QSqlQuery()
            query.prepare('select arp_bebid from arbeitsplaetze where arp_id = ?')
            query.addBindValue(wpId)
            query.exec_()
            if query.lastError().isValid():
                print('Error while selecting arp_bebid for arbeitsplatz:', query.lastError().text())
                QtGui.QMessageBox.warning(self, u'Datenbank Fehler',
                                                u'Fehler beim Laden der Dienstplan Vorlage!\n\
                                                Bitte kontaktieren Sie Ihren Administrator.')
                return
            query.next()
            bebId = query.value(0).toInt()[0]
            print('bebId', bebId, 'wpId', wpId)
            query = QtSql.QSqlQuery()
            query.prepare('select din_id from dienstnehmer where din_bebid = ? order by RAND()')
            query.addBindValue(bebId)
            query.exec_()
            if query.lastError().isValid():
                print('Error while selecting dienstnehmer:', query.lastError().text())
                QtGui.QMessageBox.warning(self, u'Datenbank Fehler',
                                                u'Fehler beim Laden der Dienstplan Vorlage!\n\
                                                Bitte kontaktieren Sie Ihren Administrator.')
                return
            
            availableEmps = []
            while query.next():
                print('BP1', query.value(0).toInt()[0])
                availableEmps.append(query.value(0).toInt()[0])
            print('availableEmps:', availableEmps)
            
            suitableEmpFound = False
            eventDate = self.getEventProperties(self.getCurrentEventId())['ver_datum'].toPyDate()
            for empId in availableEmps:
                if empId in alreadyAssignedEmps:
                    continue
                
                duty = lib.Dienst.Dienst()
                duty['die_beginn'] = begin
                duty['die_ende'] = end
                duty['die_dinid'] = empId
                dutyEarnings = duty.getEarnings()
                
                emp = lib.Dienstnehmer.Dienstnehmer(empId)
                remainingSalary = emp.getRemainingSalary(eventDate)
                
                if dutyEarnings > remainingSalary:
                    continue
                else:
                    employeeModel = waiterWidgetRefs['employeeCombo'].model()
                    idx = employeeModel.match(employeeModel.index(0, 0), 0, empId)[0]
                    waiterWidgetRefs['employeeCombo'].setCurrentIndex(idx.row())
                    suitableEmpFound = True
                    alreadyAssignedEmps.append(empId)
                    break
                
            if not suitableEmpFound:
                print('No suitable employee found for workplace %s' % wpId)
                QtGui.QMessageBox.warning(self,
                                          u'Dienstnehmer Fehler',
                                          u'Kein passender Dienstnehmer gefunden \
                                          für Arbeitsplatz %s' % wpId)
                
        self.validateRoster()
    
    def askToContinueIfModified(self):
        if self.modified:
            answer = QtGui.QMessageBox.question(self,
                                                u'Änderungen vorhanden',
                                                u'Es sind nicht gespeicherte Änderungen \
                                                vorhanden\nTrotzdem fortfahren?',
                                                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.No:
                return False
            else:
                return True
        return True
    
    def getCurrentEventId(self):
        return self.getPKForCombobox(self.ui.comboBox_event, 'ver_id')
    
    def getEventProperties(self, eventId):
        shift = lib.Schicht.Schicht(eventId)
        return shift
    
    def getEmployeeProperties(self, dinId):
        emp = lib.Dienstnehmer.Dienstnehmer(dinId)
        return emp
    
    def getWorkplaceProperties(self, arpId):
        wp = lib.Arbeitsplatz.Arbeitsplatz(arpId)
        return wp
        
    def getFieldOfEmploymentProperties(self, bebId):
        foe = Beschaeftigungsbereich(bebId)
        return foe
    
    def drawTimeTable(self):
        """delay the drawing of the time table
        this is an ugly workaround to give QT time to settle things,
        otherwise there where scaling issues of the scene within the graphicsView_timeTable
        TODO: handle that in a somehow more sane way"""
        if self.__drawTimer.isActive():
            self.__drawTimer.stop()
            
        self.__drawTimer.singleShot(500, self.reallyDrawTimeTable)
    
    def reallyDrawTimeTable(self):
        gv = self.ui.graphicsView_timeTable
        scene = QtGui.QGraphicsScene()
        gv.setScene(scene)
        
        shift = self.getEventProperties(self.getCurrentEventId())
        shiftBegin = shift['date_time']
        
        black = QtGui.QPen(QtGui.QColor(0xdd, 0xdd, 0xdd))
        red = QtGui.QPen(QtGui.QColor(0xff, 0x44, 0x44))
        red.setWidth(5)
        
        font = QtGui.QFont()
        font.setPixelSize(30)
        for x in range(18):
            time = x + shiftBegin.time().hour() - 6
            if time < 0:
                time = 24 + time
            elif time > 24:
                time = time - 24
                
            txt = scene.addSimpleText(u'%s' % time, font)
            
            x = x * 100
            txt.setPos(x, 0)
            scene.addLine(x, 0, x, 1000, black)
            
        tmpTime = shiftBegin.time()
        tmpTime.setHMS(shiftBegin.time().hour(), 0, 0)
        tmpDateTime = QtCore.QDateTime(shiftBegin)
        tmpDateTime.setTime(tmpTime)
        
        shiftBeginX = (tmpDateTime.addSecs(-6 * 3600).secsTo(shiftBegin) / 3600.0) * 100
        scene.addLine(shiftBeginX, 0, shiftBeginX, 1000, red)
        
        gv.fitInView(scene.sceneRect())
        
        for wr in self.employees:
            try:
                empProps = self.getEmployeeProperties(self.
                                                   getPKForCombobox(wr['employeeCombo'], 'din_id'))
            except ComboBoxPKError:
                continue
            
            empColor = QtGui.QColor(empProps['din_farbe'])
            complementaryColor = QtGui.QColor(255 - empColor.red(),
                                              255 - empColor.green(),
                                              255 - empColor.blue())
            brush = QtGui.QBrush(empColor)
            pen = QtGui.QPen(complementaryColor)
            
            begin = wr['beginDateTimeEdit'].dateTime()
            beginDelta = shift['date_time'].secsTo(begin) / 3600.0
            
            end = wr['endDateTimeEdit'].dateTime()
            shiftLen = begin.secsTo(end) / 3600.0
            
            x = shiftBeginX + beginDelta * 100
            
            point = wr['frame'].mapToGlobal(QtCore.QPoint(0, 0))
            y = gv.mapToScene(gv.mapFromGlobal(point)).y() + 30
            scene.addRect(x, y, shiftLen * 100, 50, pen, brush)
            
            font.setPixelSize(30)
            font.setBold(True)
            txt = scene.addText(u'%s' % empProps['din_name'], font)
            txt.setPos(x + 5, y + 5)
            txt.setDefaultTextColor(complementaryColor)
        
        gv.fitInView(scene.itemsBoundingRect())
    
    def resizeEvent(self, event):
        super(DienstplanForm, self).resizeEvent(event)
        self.drawTimeTable()
    
    def onFrameShown(self, frame, event):
        super(QtGui.QFrame, frame).showEvent(event)
        self.drawTimeTable()
