# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

class NullDelegate(QtSql.QSqlRelationalDelegate):
	"""this class allows to insert null values into the database table"""
	
	def setModelData(self, editor, model, index):

		if editor.inherits('QLineEdit'):
			record = model.database().record(model.tableName())
			field = record.field(index.column())
			value = editor.property('text')	

			#optional required status means the column is nullable
			if unicode(value.toString()) == u'' and field.requiredStatus() == QtSql.QSqlField.Optional:
				value = QtCore.QVariant()
			
			model.setData(index, value)
		else:
			QtSql.QSqlRelationalDelegate.setModelData(self, editor, model, index)



