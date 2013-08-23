# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

from CONSTANTS import *
import DBConnection
import config

from forms.formBase import FormBase
from ui.forms.dienstplanForm_gui import Ui_DienstplanForm

from sets import Set
import datetime
import calendar
import sip

NACHTZUSCHLAG = 21.0
TRINKGELDPAUSCHALE = 1.5
MINHOURSFORPAUSE = 6.0

class DienstplanForm(FormBase):
	
	uiClass = Ui_DienstplanForm
	ident = 'dienstplan'
	
	def __init__(self, parent):
		self.employees = []
		self.modified = False
		self.unmodifiedEmpCombos = []
		super(DienstplanForm, self).__init__(parent)
		self.load()
	
	
	def setupUi(self):
		super(DienstplanForm, self).setupUi()
		eventsModel = QtSql.QSqlTableModel()
		eventsModel.setTable('veranstaltungen')
		eventsModel.setSort(eventsModel.fieldIndex('ver_datum'), QtCore.Qt.DescendingOrder)
		eventsModel.select()
		
		view = QtGui.QTableView()
		view.setModel(eventsModel)

		#Do with the view whatever you like
		view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		view.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		view.setAutoScroll(False)
		view.resizeColumnsToContents()
		view.resizeRowsToContents()
		#view.setSortingEnabled(True)
		view.verticalHeader().setVisible(False) #Rownumbers 
		view.setMinimumWidth(view.horizontalHeader().length())
		view.setColumnHidden(0, True)
		view.setColumnHidden(4, True)

		#The important part: First set the model, then the view on the box
		#box.setModel(model)
		#box.setView(view)
		
		self.ui.comboBox_event.setModel(eventsModel)
		self.ui.comboBox_event.setView(view)
		self.ui.comboBox_event.setModelColumn(eventsModel.fieldIndex('ver_bezeichnung'))
		
		templateModel = QtSql.QSqlQueryModel()
		templateModel.setQuery('select distinct div_bezeichnung from dienste_vorlagen')
		self.ui.comboBox_template.setModel(templateModel)
		#self.ui.comboBox_template.setModelColumn(1)
		
		
		
		
	def setupSignals(self):
		super(DienstplanForm, self).setupSignals()
		self.connect(self.ui.pushButton_addEmployee, QtCore.SIGNAL('clicked()'), lambda: self.setModified(True) and self.addEmployee())
		self.connect(self.ui.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)
		self.connect(self.ui.buttonBox, QtCore.SIGNAL('rejected()'), self.reject)
		self.connect(self.ui.buttonBox, QtCore.SIGNAL('clicked(QAbstractButton *)'), self.onButtonBoxClicked)
		self.connect(self.ui.comboBox_event, QtCore.SIGNAL('currentIndexChanged(int)'), self.load)
		self.connect(self.ui.pushButton_saveTemplate, QtCore.SIGNAL('clicked()'), self.saveTemplate)
		self.connect(self.ui.pushButton_loadTemplate, QtCore.SIGNAL('clicked()'), self.loadTemplate)
		self.connect(self.ui.pushButton_autoAssignEmps, QtCore.SIGNAL('clicked()'), self.autoAssignEmployees)
		
		
		
		
	def addEmployee(self, dinId=None, arpId=None, dieBeginn=None, dieEnde=None, diePause=None):
		#widget = QtGui.QWidget()
		eventProps = self.getEventProperties(self.getCurrentEventId())
		layout = QtGui.QVBoxLayout()
		workLayout = QtGui.QHBoxLayout()
		
		workplaceModel = QtSql.QSqlTableModel()
		workplaceModel.setTable('arbeitsplaetze')
		workplaceModel.select()
		workplaceCombo = QtGui.QComboBox()
		workplaceCombo.setModel(workplaceModel)
		workplaceCombo.setModelColumn(workplaceModel.fieldIndex('arp_bezeichnung'))
		workLayout.addWidget(workplaceCombo)
		
		employeeModel = QtSql.QSqlTableModel()
		employeeModel.setTable('dienstnehmer')
		employeeModel.select()
		employeeCombo = QtGui.QComboBox()
		employeeCombo.setModel(employeeModel)
		employeeCombo.setModelColumn(employeeModel.fieldIndex('din_name'))
		workLayout.addWidget(employeeCombo)
		
		layout.addLayout(workLayout)
		
		beginDateTimeEdit = QtGui.QDateTimeEdit()
		beginDateTimeEdit.setCalendarPopup(True)
		beginDateTimeEdit.setMinimumDate(eventProps['ver_datum'])
		beginDateTimeEdit.setMaximumDate(eventProps['ver_datum'].addDays(1))
		
		endDateTimeEdit = QtGui.QDateTimeEdit()
		endDateTimeEdit.setCalendarPopup(True)
		endDateTimeEdit.setMinimumDate(eventProps['ver_datum'])
		endDateTimeEdit.setMaximumDate(eventProps['ver_datum'].addDays(1))
		
		pauseCheckBox = QtGui.QCheckBox()
		pauseCheckBox.setText(u'Pause')
		timeLayout = QtGui.QHBoxLayout()
		timeLayout.addWidget(beginDateTimeEdit)
		timeLayout.addWidget(endDateTimeEdit)
		timeLayout.addWidget(pauseCheckBox)
		layout.addLayout(timeLayout)
		
		delBtn = QtGui.QPushButton(u'löschen')
		layout.addWidget(delBtn)
		
		frame = QtGui.QFrame()
		frame.setFrameShape(QtGui.QFrame.Box)
		#frame.setFrameShadow(QtGui.QFrame.Sunken)
		frame.setLayout(layout)
		#insert before the push button; -2 because there are already 2 widget in the layout: the button and the spacer
		self.ui.verticalLayout_employees.insertWidget(self.ui.verticalLayout_employees.count()-2, frame)
		
		widgetRef = { 	'workplaceCombo': workplaceCombo,
						'employeeCombo': employeeCombo,
						'beginDateTimeEdit': beginDateTimeEdit,
						'endDateTimeEdit': endDateTimeEdit,
						'pauseCheckBox': pauseCheckBox,
						'frame': frame
					}
		
		if arpId is not None:
			idx = workplaceModel.match(workplaceModel.index(0,0), 0, arpId)[0]
			workplaceCombo.setCurrentIndex(idx.row())
			
		self.checkEmployeeWorkplaceAssignment(widgetRef)
			
		if dinId is not None:
			idx = employeeModel.match(employeeModel.index(0,0), 0, dinId)[0]
			employeeCombo.setCurrentIndex(idx.row())
		else:
			self.unmodifiedEmpCombos.append(widgetRef['employeeCombo'])
			
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
		else:
			endDateTimeEdit.setDate(eventProps['ver_datum'])
			endDateTimeEdit.setTime(eventProps['ver_beginn'])
			
		if diePause is not None and diePause > 0.001 :
			pauseCheckBox.setChecked(QtCore.Qt.Checked)
		
		self.setEmployeeFrameColor(widgetRef)
		
		
		self.connect(workplaceCombo, QtCore.SIGNAL('currentIndexChanged(int)'), lambda: self.setModified(True))
		self.connect(employeeCombo, QtCore.SIGNAL('currentIndexChanged(int)'), lambda: self.setModified(True))
		self.connect(beginDateTimeEdit, QtCore.SIGNAL('dateTimeChanged (const QDateTime&)'), lambda: self.setModified(True))
		self.connect(endDateTimeEdit, QtCore.SIGNAL('dateTimeChanged (const QDateTime&)'), lambda: self.setModified(True))
		self.connect(pauseCheckBox, QtCore.SIGNAL('stateChanged(int)'), lambda: self.setModified(True))
		
		self.connect(delBtn, QtCore.SIGNAL('clicked()'), lambda f=frame, wr=widgetRef: self.deleteWidget(f) and self.employees.remove(wr))
		
		self.connect(employeeCombo, QtCore.SIGNAL('currentIndexChanged(int)'), lambda i, wr=widgetRef: self.checkEmployeeHours(wr))
		self.connect(beginDateTimeEdit, QtCore.SIGNAL('dateTimeChanged (const QDateTime&)'), lambda dt, wr=widgetRef: self.checkEmployeeHours(wr))
		self.connect(endDateTimeEdit, QtCore.SIGNAL('dateTimeChanged (const QDateTime&)'), lambda dt, wr=widgetRef: self.checkEmployeeHours(wr))
		self.connect(pauseCheckBox, QtCore.SIGNAL('stateChanged(int)'), lambda i, wr=widgetRef: self.checkEmployeeHours(wr))
		
		self.connect(beginDateTimeEdit, QtCore.SIGNAL('dateTimeChanged (const QDateTime&)'), lambda dt, wr=widgetRef: self.checkDateTime(wr))
		self.connect(endDateTimeEdit, QtCore.SIGNAL('dateTimeChanged (const QDateTime&)'), lambda dt, wr=widgetRef: self.checkDateTime(wr))
		
		self.connect(employeeCombo, QtCore.SIGNAL('currentIndexChanged(int)'), lambda i, wr=widgetRef: self.setEmployeeFrameColor(wr))
		self.connect(employeeCombo, QtCore.SIGNAL('currentIndexChanged(int)'), lambda i, wr=widgetRef: (wr['employeeCombo'] in self.unmodifiedEmpCombos) and self.unmodifiedEmpCombos.remove(wr['employeeCombo']))
		self.connect(workplaceCombo, QtCore.SIGNAL('currentIndexChanged(int)'), lambda i, wr=widgetRef: self.checkEmployeeWorkplaceAssignment(wr))
		
		self.employees.append(widgetRef)
		self.checkDateTime(widgetRef)
		
		return widgetRef
	
	
	def findEmployeeWidgetRefByEmpId(self, empId):
		for emp in self.employees:
			id_ = self.getPKForCombobox(emp['employeeCombo'], 'din_id')
			print 'empId:', empId, 'cbId:', id_
			if id_ == empId:
				return emp
	
	
	def setModified(self, state=True):
		self.modified = state
		return True
	
		
	def validateRoster(self):
		
		def get_duplicate_items( L ):
			new = Set()
			for item in L:
				if L.count(item) > 1:
					new.add( item )
			return list(new)
		
		print "validateRoster"
		employeesInUse = []
		workplacesInUse = []
		for waiterWidgetRefs in self.employees:
			empId = self.getPKForCombobox(waiterWidgetRefs['employeeCombo'], 'din_id')
			employeesInUse.append(empId)
			
			#wpId = self.getPKForCombobox(waiterWidgetRefs['workplaceCombo'], 'arp_id')
			#workplacesInUse.append(wpId)
			
		duplicateWaiters = get_duplicate_items(employeesInUse)
		#duplicateWorkplaces = get_duplicate_items(workplacesInUse)
		
		if len(duplicateWaiters):
			QtGui.QMessageBox.warning(self, u'Doppelte Einteilung', 
											u'Der/die Kellner %s wurde doppelt eingeteilt'%duplicateWaiters)
			return False

		#if len(duplicateWorkplaces):
		#	QtGui.QMessageBox.warning(self, u'Doppelte Einteilung', 
		#									u'Der/die Arbeitsplatz/Artbeitsplätze %s wurde doppelt eingeteilt'%duplicateWorkplaces)
		#	return False
		
		#print duplicateWaiters, duplicateWorkplaces
		
		failingEmployees = self.checkMonthlyWorkingHours(employeesInUse)
		if len(failingEmployees) > 0:
			QtGui.QMessageBox.warning(self, u'Arbeitszeitüberschreitung', 
											u'Folgende Dienstnehmer überschreiten ihre monatliche Arbeitszeit: %s'%failingEmployees)
			return False
		
		return True
			
			
		
	def checkMonthlyWorkingHours(self, empIds):
		print "checkMonthlyWorkingHours"
		eventProps = self.getEventProperties(self.getCurrentEventId())
		eventDate = eventProps['ver_datum'].toPyDate()
		failingEmployees = []
		for empId in empIds:
			remainingHours = self.getRemainingEmployeeHours(empId, eventDate)
			widgetRef = self.findEmployeeWidgetRefByEmpId(empId)
			beginDate = widgetRef['beginDateTimeEdit'].dateTime().toPyDateTime()
			endDate = widgetRef['endDateTimeEdit'].dateTime().toPyDateTime()
			delta = endDate-beginDate
			days, seconds = delta.days, delta.seconds
			hours = days*24.0 + seconds/3600.0
			print "hours:", hours, "remainingHours", remainingHours, 'beginDate:', beginDate, 'endDate:', endDate, 'days:', days, 'seconds:', seconds
			if hours > remainingHours:
				empProps = self.getEmployeeProperties(empId)
				failingEmployees.append((empProps['din_id'], empProps['din_name'], 'Verbleibende Stunden: %s'%remainingHours))
			
		return failingEmployees
	
	
	def checkEmployeeHours(self, widgetRef):
		print "checkEmployeeHours"
		combo = widgetRef['employeeCombo']
		empId = self.getPKForCombobox(combo, 'din_id')
		failed = self.checkMonthlyWorkingHours([empId])
		if len(failed) > 0:
			combo.setStyleSheet('QFrame {background-color:red;}')
		else:
			combo.setStyleSheet('')
			
		
	
	
	def getRemainingEmployeeHours(self, dinId, date=None):
		"""
		@dinId the employee ID
		@date supply a date within the month the hours are wanted
		"""
		if date is None:
			date = datetime.datetime.now()
			
		year = date.year
		month = date.month
		lastDay = calendar.monthrange(year, month)[1]
		monthBegin = datetime.date(year, month, 1)
		monthEnd = datetime.date(year, month, lastDay)
			
		query = QtSql.QSqlQuery()
		query.prepare("""
						select sum(time_to_sec(timediff(die_ende, die_beginn))/3600), count(*) as c
						from dienste
						where 1=1
						and die_dinid = ?
						and die_beginn between ? and ?
						and die_verid != ?
						""")
		query.addBindValue(dinId)
		query.addBindValue(QtCore.QDateTime(monthBegin))
		query.addBindValue(QtCore.QDateTime(monthEnd))
		query.addBindValue(self.getCurrentEventId())
		
		query.exec_()
		if query.lastError().isValid():
			print 'Error while selecting employee hours:', query.lastError().text()
			QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
											u'Fehler beim Berechnen der Monatsstunden!\nBitte kontaktieren Sie Ihren Administrator.')
			return False
		
		query.next()
		
		hours = query.value(0).toFloat()[0]
		count = query.value(1).toInt()[0]
		
		empProps = self.getEmployeeProperties(dinId)
		print empProps
		salary = empProps['din_gehalt']
		hourlyRate = empProps['din_stundensatz']
		
		remainingSalary = salary - hours*hourlyRate - NACHTZUSCHLAG*count - TRINKGELDPAUSCHALE*count
		remainingHours = (remainingSalary - NACHTZUSCHLAG - TRINKGELDPAUSCHALE)/hourlyRate
		
		print 'dinId:', dinId, 'month hours:', hours, 'count:', count, 'remainingHours:', remainingHours
		
		return remainingHours
	
	
	def checkDateTime(self, wr):
		begin = wr['beginDateTimeEdit'].dateTime()
		end = wr['endDateTimeEdit'].dateTime()
		modified = False
		if end <= begin:
			wpId = self.getPKForCombobox(wr['workplaceCombo'], 'arp_id')
			wpProps = self.getWorkplaceProperties(wpId)
			wr['endDateTimeEdit'].setDateTime(begin.addSecs(int(wpProps['arp_std_dienst_dauer']*3600)))
			modified = True
			QtGui.QMessageBox.warning(self, u'Zeiten Fehler', 
											u'Das End-Datum liegt vor dem Beginn-Datum! Zeitraum wurde angepasst.')
			
		delta = end.toPyDateTime()-begin.toPyDateTime()
		if delta.days > 0 or delta.seconds/3600.0 > (MINHOURSFORPAUSE-0.01):
			if not wr['pauseCheckBox'].isChecked():
				wr['pauseCheckBox'].setChecked(True)
				modified = True
		else:
			if wr['pauseCheckBox'].isChecked():
				wr['pauseCheckBox'].setChecked(False)
				modified = True
		
		if modified:
			self.setModified()
			
			
	def checkEmployeeWorkplaceAssignment(self, wr):
		wpProps = self.getWorkplaceProperties(self.getPKForCombobox(wr['workplaceCombo'], 'arp_id'))
		wr['employeeCombo'].model().setFilter('dienstnehmer.din_bebid = %s'%wpProps['arp_bebid'])
		
	
	
	def setEmployeeFrameColor(self, wr):
		empProps = self.getEmployeeProperties(self.getPKForCombobox(wr['employeeCombo'], 'din_id'))
		color = empProps['din_farbe']
		print 'color:', empProps['din_farbe'], 'background-color:%s;'%color
		wr['frame'].setStyleSheet('QFrame {background-color:%s;}'%color)
		
		
		
	def accept(self):
		if not self.modified or self.save():
			super(DienstplanForm, self).accept()
		
	def save(self):
		if not self.validateRoster():
			return False
		
		if len(self.unmodifiedEmpCombos):
			answer = QtGui.QMessageBox.question(self, u'Dienstnehmer nicht modifiziert', 
													u'Ein oder mehrere Dienstnehmer Drop-Downs wurden nicht verändert.\nTrotzdem fortfahren?',
													QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if answer == QtGui.QMessageBox.No:
				return False
			else:
				self.unmodifiedEmpCombos = []
		
		try:
			self.beginTransaction()
			eventId = self.getPKForCombobox(self.ui.comboBox_event, 'ver_id')
			
			query = QtSql.QSqlQuery()
			query.prepare("delete from dienste where die_verid = ?")
			query.addBindValue(eventId)
			query.exec_()
			if query.lastError().isValid():
				self.rollback()
				print 'Error while deleting dienstplan for event:', query.lastError().text()
				QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
												u'Fehler beim Speichern des Dienstplans!\nBitte kontaktieren Sie Ihren Administrator.')
				return False
			
			
			for waiterWidgetRefs in self.employees:
				empId = self.getPKForCombobox(waiterWidgetRefs['employeeCombo'], 'din_id')
				wpId = self.getPKForCombobox(waiterWidgetRefs['workplaceCombo'], 'arp_id')
				begin = waiterWidgetRefs['beginDateTimeEdit'].dateTime()
				end = waiterWidgetRefs['endDateTimeEdit'].dateTime()
				pause = 0.5 if waiterWidgetRefs['pauseCheckBox'].isChecked() else 0.0
				
				query = QtSql.QSqlQuery()
				query.prepare("""
								insert into dienste (die_dinid, die_verid, die_arpid, die_beginn, die_ende, die_pause)
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
					print 'Error while inserting dienstplan:', query.lastError().text()
					QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
													u'Fehler beim Speichern des Dienstplans!\nBitte kontaktieren Sie Ihren Administrator.')
					return False
				
			self.commit()
		except Exception as e:
			print "exception in save()", e
			self.rollback()
		
		self.setModified(False)
		return True
			
			
	def load(self):
		print "load"
		if not self.askToContinueIfModified():
			return False
		
		self.clear()
		
		eventId = self.getCurrentEventId()
		print "event:", eventId
		query = QtSql.QSqlQuery()
		query.prepare("select die_id, die_dinid, die_arpid, die_beginn, die_ende, die_pause from dienste where die_verid = ?")
		query.addBindValue(eventId)
		query.exec_()
		if query.lastError().isValid():
			print 'Error while selecting dienstplan:', query.lastError().text()
			QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
											u'Fehler beim Laden des Dienstplans!\nBitte kontaktieren Sie Ihren Administrator.')
			return False
		
		while query.next():
			dieId = query.value(0).toInt()[0]
			dinId = query.value(1).toInt()[0]
			arpId = query.value(2).toInt()[0]
			dieBeginn = query.value(3).toDateTime()
			dieEnde = query.value(4).toDateTime()
			diePause = query.value(5).toFloat()[0]
			
			self.addEmployee(dinId, arpId, dieBeginn, dieEnde, diePause)
			
		self.setModified(False)
		
	def onButtonBoxClicked(self, btn):
		if self.ui.buttonBox.buttonRole(btn) == QtGui.QDialogButtonBox.ApplyRole:
			if self.modified:
				if self.save():
					QtGui.QMessageBox.information(self, u'Speichern erfolgreich', 
												u'Änderungen erfolgreich gespeichert.')
				else:
					QtGui.QMessageBox.warning(self, u'Speichern nicht erfolgreich', 
											u'Fehler beim Speichern des Dienstplans!\nBitte kontaktieren Sie Ihren Administrator.')
				
	
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
		name, ok = QtGui.QInputDialog.getText(self, u'Vorlagenname', u'Bitte gib einen Namen für die Vorlage ein', QtGui.QLineEdit.Normal, self.ui.comboBox_template.currentText())
		if ok:
			query = QtSql.QSqlQuery()
			query.prepare('select count(*) from dienste_vorlagen where div_bezeichnung = ?')
			query.addBindValue(name)
			query.exec_()
			if query.lastError().isValid():
				print 'Error while selecting dienste_vorlagen:', query.lastError().text()
				QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
												u'Fehler beim Selektieren der Dienstvorlagen!\nBitte kontaktieren Sie Ihren Administrator.')
				return False
			query.next()
			count = query.value(0).toInt()[0]
			
			if count > 0:
				answer = QtGui.QMessageBox.question(self, u'Vorlage existiert', 
														u'Die Vorlage %s wird überschrieben. Sind Sie sicher?.'%unicode(name),
														QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
				if answer == QtGui.QMessageBox.No:
					return False
			
			try:
				self.beginTransaction()
				
				query = QtSql.QSqlQuery()
				query.prepare('delete from dienste_vorlagen where div_bezeichnung = ?')
				query.addBindValue(name)
				query.exec_()
				if query.lastError().isValid():
					print 'Error while deleting dienste_vorlagen:', query.lastError().text()
					QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
													u'Fehler beim Löschen der Dienstvorlagen!\nBitte kontaktieren Sie Ihren Administrator.')
					raise Exception()
				
				
				for waiterWidgetRefs in self.employees:
					wpId = self.getPKForCombobox(waiterWidgetRefs['workplaceCombo'], 'arp_id')
					begin = waiterWidgetRefs['beginDateTimeEdit'].time()
					end = waiterWidgetRefs['endDateTimeEdit'].time()
					
					query = QtSql.QSqlQuery()
					query.prepare("""
									insert into dienste_vorlagen (div_bezeichnung, div_arpid, div_beginn, div_ende)
									values (?, ?, ?, ?)
									""")
					query.addBindValue(name)
					query.addBindValue(wpId)
					query.addBindValue(begin)
					query.addBindValue(end)
					query.exec_()
					if query.lastError().isValid():
						print 'Error while inserting dienstplan template:', query.lastError().text()
						QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
														u'Fehler beim Speichern der Dienstplan Vorlage!\nBitte kontaktieren Sie Ihren Administrator.')
						raise Exception()
			
			except Exception as e:
				self.rollback()
				print e
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
		query.prepare('select div_id, div_bezeichnung, div_arpid, div_beginn, div_ende from dienste_vorlagen where div_bezeichnung = ?')
		query.addBindValue(tmplName)
		query.exec_()
		if query.lastError().isValid():
			print 'Error while getting dienstplan template:', query.lastError().text()
			QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
											u'Fehler beim Laden der Dienstplan Vorlage!\nBitte kontaktieren Sie Ihren Administrator.')
		while query.next():
			wpId = query.value(2).toInt()[0]
			begin = query.value(3).toTime()
			end = query.value(4).toTime()
			wr = self.addEmployee(arpId=wpId, dieBeginn=begin, dieEnde=end)
			#self.checkDateTime(wr)
		
		self.autoAssignEmployees()
		self.setModified()
		
		
	def autoAssignEmployees(self):
		alreadyAssignedEmps = []
		
		for waiterWidgetRefs in self.employees:
			wpId = self.getPKForCombobox(waiterWidgetRefs['workplaceCombo'], 'arp_id')
			begin = waiterWidgetRefs['beginDateTimeEdit'].dateTime()
			end = waiterWidgetRefs['endDateTimeEdit'].dateTime()
			delta = end.toPyDateTime()-begin.toPyDateTime()
			days, seconds = delta.days, delta.seconds
			workHours = days*24.0 + seconds/3600.0
			
			query = QtSql.QSqlQuery()
			query.prepare('select arp_bebid from arbeitsplaetze where arp_id = ?')
			query.addBindValue(wpId)
			query.exec_()
			if query.lastError().isValid():
				print 'Error while selecting arp_bebid for arbeitsplatz:', query.lastError().text()
				QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
												u'Fehler beim Laden der Dienstplan Vorlage!\nBitte kontaktieren Sie Ihren Administrator.')
				return
			query.next()
			bebId = query.value(0).toInt()[0]
			print 'bebId', bebId, 'wpId', wpId
			query = QtSql.QSqlQuery()
			query.prepare('select din_id from dienstnehmer where din_bebid = ? order by RAND()')
			query.addBindValue(bebId)
			query.exec_()
			if query.lastError().isValid():
				print 'Error while selecting dienstnehmer:', query.lastError().text()
				QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
												u'Fehler beim Laden der Dienstplan Vorlage!\nBitte kontaktieren Sie Ihren Administrator.')
				return
			
			availableEmps = []
			while query.next():
				print 'BP1', query.value(0).toInt()[0]
				availableEmps.append(query.value(0).toInt()[0])
			print 'availableEmps:', availableEmps
			
			suitableEmpFound = False
			eventDate = self.getEventProperties(self.getCurrentEventId())['ver_datum'].toPyDate()
			for empId in availableEmps:
				if empId in alreadyAssignedEmps:
					continue
				remainingHours = self.getRemainingEmployeeHours(empId, eventDate)
				print "workHours:", workHours, 'remainingHours:', remainingHours, 'empId:', empId, 'eventDate:', eventDate
				if workHours > remainingHours:
					continue
				else:
					employeeModel = waiterWidgetRefs['employeeCombo'].model()
					idx = employeeModel.match(employeeModel.index(0,0), 0, empId)[0]
					waiterWidgetRefs['employeeCombo'].setCurrentIndex(idx.row())
					suitableEmpFound = True
					alreadyAssignedEmps.append(empId)
					break
				
			if not suitableEmpFound:
				print 'No suitable employee found for workplace %s'%wpId
				QtGui.QMessageBox.warning(self, u'Dienstnehmer Fehler', 
												u'Kein passender Dienstnehmer gefunden für Arbeitsplatz %s'%wpId)
				
		self.validateRoster()
				
			
			
	
	def askToContinueIfModified(self):
		if self.modified:
			answer = QtGui.QMessageBox.question(self, u'Änderungen vorhanden', 
													u'Es sind nicht gespeicherte Änderungen vorhanden\nTrotzdem fortfahren?',
													QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if answer == QtGui.QMessageBox.No:
				return False
			else:
				return True
		return True
	
		
	
	def getCurrentEventId(self):
		return self.getPKForCombobox(self.ui.comboBox_event, 'ver_id')
	
		
	def getEventProperties(self, eventId):
		query = QtSql.QSqlQuery()
		query.prepare("select ver_id, ver_datum, ver_bezeichnung, ver_beginn, ver_checkpointid from veranstaltungen where ver_id = ?")
		query.addBindValue(eventId)
		query.exec_()
		if query.lastError().isValid():
			print 'Error while selecting dienstplan:', query.lastError().text()
			QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
											u'Fehler beim Laden des Dienstplans!\nBitte kontaktieren Sie Ihren Administrator.')
			return False
		
		query.next()
		
		props = {
				'ver_id': query.value(0).toInt()[0],
				'ver_datum': query.value(1).toDate(),
				'ver_bezeichnung': query.value(2).toString(),
				'ver_beginn': query.value(3).toTime(),
				'ver_checkpointid': query.value(4).toInt()[0]
				}
		
		return props
	
	def getEmployeeProperties(self, dinId):
		query = QtSql.QSqlQuery()
		query.prepare("""select din_id, din_name, din_gehalt, din_bebid, din_stundensatz, din_farbe from dienstnehmer where din_id = ?""")
		query.addBindValue(dinId)
		query.exec_()
		if query.lastError().isValid():
			print 'Error while selecting dienstnehmer:', query.lastError().text()
			QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
											u'Fehler beim Laden des Dienstnehmers!\nBitte kontaktieren Sie Ihren Administrator.')
			return False
		
		query.next()
		
		props = {
				'din_id': query.value(0).toInt()[0],
				'din_name': query.value(1).toString(),
				'din_gehalt': query.value(2).toFloat()[0],
				'din_bebid': query.value(3).toInt()[0],
				'din_stundensatz': query.value(4).toFloat()[0],
				'din_farbe': query.value(5).toString()
				}
		
		return props
	
	def getWorkplaceProperties(self, arpId):
		query = QtSql.QSqlQuery()
		query.prepare("""select arp_id, arp_bezeichnung, arp_std_dienst_dauer, arp_bebid from arbeitsplaetze where arp_id = ?""")
		query.addBindValue(arpId)
		query.exec_()
		if query.lastError().isValid():
			print 'Error while selecting arbeitsplaetze:', query.lastError().text()
			QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
											u'Fehler beim Laden des Arbeitsplatzes!\nBitte kontaktieren Sie Ihren Administrator.')
			return False
		
		query.next()
		
		props = {
				'arp_id': query.value(0).toInt()[0],
				'arp_bezeichnung': query.value(1).toString(),
				'arp_std_dienst_dauer': query.value(2).toFloat()[0],
				'arp_bebid': query.value(3).toInt()[0]
				}
		
		return props
		
		
		
		