# -*- coding: utf-8 -*-
import sqlite3
import decimal
import sys

from PyQt4 import QtCore, QtGui, QtSql

from ui.lieferantenDlg_gui import Ui_LieferantenDialog

from CONSTANTS import *

sqlite3.register_adapter(decimal.Decimal, lambda x:float(x))
sqlite3.register_converter('decimal', decimal.Decimal)


class LieferantenDialog(QtGui.QDialog):
	
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)

		self.ui = Ui_LieferantenDialog()

		self.ui.setupUi(self)
		
		self._connectToDb()
		
		self._setupForm()
		
	
	
	def _setupForm(self):
		# column headers
		self.model.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
		self.model.setHeaderData(1, QtCore.Qt.Horizontal, 'Name')
		

		
		# table view
		# ------------------------------------------------
		self.tableView = self.ui.tableView_lieferanten
		self.tableView.setModel(self.model)
		self.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.tableView))
		self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.tableView.resizeColumnsToContents()
		self.tableView.horizontalHeader().setStretchLastSection(True)
		
		self.connect(self.ui.pushButton_OK, QtCore.SIGNAL('clicked()'), self._onOKBtnClicked)
		self.connect(self.ui.pushButton_newRecord, QtCore.SIGNAL('clicked()'), self._onNewRecordBtnClicked)
		self.connect(self.ui.pushButton_deleteRecord, QtCore.SIGNAL('clicked()'), self._onDeleteRecordBtnClicked)
		
		
		
	def _onOKBtnClicked(self):
		self.accept()
		
		
	
	def _onNewRecordBtnClicked(self):
		rec = self.model.record()
		rec.setValue(1, '')
		self.model.insertRecord(-1, rec)
		
		
	def _onDeleteRecordBtnClicked(self):
		selected = self.tableView.selectionModel().selectedRows(0)
		for i in range(len(selected)):
			self.model.removeRows(selected[i].row(), 1)
		self.model.submitAll()
			
			
			
	def _connectToDb(self):
		self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
		self.db.setHostName(DBHOST)
		self.db.setDatabaseName(DBNAME)
		self.db.setPassword(DBPASSWORD)
		self.db.setUserName(DBUSER)
		ok = self.db.open()  
		self.model = QtSql.QSqlTableModel()
		self.model.setTable('lieferanten')
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()
		#print self.model.select()
		
		
			
			
			
if __name__ == "__main__":
	SQLITEDB = 'WaWi.db'
	
	app = QtGui.QApplication(sys.argv)
	win = LieferantenDialog()
	win.show()
	sys.exit(app.exec_())
