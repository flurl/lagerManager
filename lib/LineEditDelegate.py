# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql

class LineEditDelegate(QtGui.QStyledItemDelegate):

    def __init__(self, nullable=False):
        self.nullable = nullable
        super(LineEditDelegate, self).__init__()

    def createEditor(self, parent, option, index):
        line_edit = QtGui.QLineEdit(parent)
        return line_edit
        
        
    def setModelData(self, editor, model, index):
        record = model.database().record(model.tableName())
        field = record.field(index.column())
        value = editor.property('text')	

        #optional required status means the column is nullable
        if self.nullable and unicode(value.toString()) == u'' and field.requiredStatus() == QtSql.QSqlField.Optional:
            value = QtCore.QVariant()

        model.setData(index, value)


