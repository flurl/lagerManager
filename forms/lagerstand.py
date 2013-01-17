# -*- coding: utf-8 -*-
import decimal
import sys

from PyQt4 import QtCore, QtGui, QtSql

from forms.formBase import FormBase
from ui.forms.lagerstandForm_gui import Ui_LagerstandForm
import config


class LagerstandForm(FormBase):
	
	uiClass = Ui_LagerstandForm
	ident = 'lagerstand'
	
	
	def setupUi(self):
		super(LagerstandForm, self).setupUi()
	
		self.model = QtSql.QSqlRelationalTableModel()
		self.model.setTable('lagerstand')
		self.model.setRelation(1, QtSql.QSqlRelation('artikel_basis', 'artikel_id', 'artikel_bezeichnung'))
		self.model.setRelation(3, QtSql.QSqlRelation('perioden', 'periode_id', 'periode_bezeichnung'))
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()

		self.setFilter()
	
		# column headers
		self.model.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
		self.model.setHeaderData(1, QtCore.Qt.Horizontal, 'Artikel')
		self.model.setHeaderData(2, QtCore.Qt.Horizontal, 'Anzahl')
		self.model.setHeaderData(3, QtCore.Qt.Horizontal, 'Periode')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView_lagerstand
		self.tableView.setModel(self.model)
		self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.horizontalHeader().setStretchLastSection(True)
		
		self.connect(self.ui.pushButton_OK, QtCore.SIGNAL('clicked()'), self._onOKBtnClicked)
		self.connect(self.ui.pushButton_initPeriod, QtCore.SIGNAL('clicked()'), self._onInitPeriodBtnClicked)
		self.connect(self.ui.comboBox_period, QtCore.SIGNAL('currentIndexChanged(int)'), self.setFilter)
		
		
		
	def _onOKBtnClicked(self):
		self.accept()
		
		
	def _onInitPeriodBtnClicked(self):
		query = QtSql.QSqlQuery()
		query.prepare("""insert into lagerstand (artikel_id, anzahl, periode_id)
					select lager_artikel_artikel, 0, lager_artikel_periode from lager_artikel where lager_artikel_periode = ?""")
		query.addBindValue(self.getCurrentPeriodId())
		query.exec_()
		query.next()
		
		if query.lastError().isValid():
			self.rollback()
			print 'Error while setting initial lagerstand:', query.lastError().text()
			QtGui.QMessageBox.warning(self, u'Datenbank Fehler', 
									'Initialer Lagerstand konnte nicht gesetzt werden!\nBitte kontaktieren Sie Ihren Administrator.')
		else:
			self.commit()
			
		self.model.select()
		
			
			
	def setFilter(self):
		self.model.setFilter('lagerstand.periode_id=%(perId)s and artikel_periode=%(perId)s'%{'perId':self.getCurrentPeriodId()})
		self.model.select()
			
			
if __name__ == "__main__":
	SQLITEDB = 'WaWi.db'
	
	app = QtGui.QApplication(sys.argv)
	win = LagerstandDialog()
	win.show()
	sys.exit(app.exec_())
