# -*- coding: utf-8 -*-
import collections

from PyQt4 import QtCore, QtGui, QtSql

from reports.textReport import TextReport
from ui.reports.defaultTableReport_gui import Ui_DefaultTableReport

class TableReport(TextReport):
    uiClass = Ui_DefaultTableReport

    def __init__(self, parent):
        TextReport.__init__(self, parent)
        self.ui.tableView.setSortingEnabled(True)
        
        
    def keyPressEvent(self, e):
        if e.modifiers() and QtCore.Qt.ControlModifier and e.key() == QtCore.Qt.Key_C:
            print 'control-c is pressed'
            self.copySelectionToClipboard()


    def process(self):
        #elements = []
        #elements.append(Heading(self.__header))
        #elements.append(self.processData())
        #elements.append(Footer(self.__footer))

        #self.ui.textView.setText(''.join(unicode(e) for e in elements))
        self.ui.tableView.setModel(self.processData())

    def processData(self):
        #output = u''
        #output += u'<table border="1">'

        model = QtGui.QStandardItemModel()
        #blankLine = False

        rowNumber = 0
        for row in self._data:
            #output += u'<tr>'
            columnNumber = 0
            for cell in row:
                if cell is None:
                    #output += u'<td>' + u'☭' * 10 + u'</td>'
                    #blankLine = True
                    cell = u'☭' * 10
                else:
                    # apply formating
                    if type(cell) is list or type(cell) is tuple:
                        if cell[1] == 'strong':
	                        #cell = (u'<strong>' + unicode(cell[0]) +
	                        #		u'</strong>')
	                        cell = cell[0]
                    #output += u'<td>%s</td>' % (cell,)

                item = QtGui.QStandardItem(unicode(cell))
                model.setItem(rowNumber, columnNumber, item)
                columnNumber += 1
            rowNumber += 1

            #output += u'</tr>'

            #if blankLine:
            #	blankLine = False
            #	output += self.mkTableHeaders()

        #output += u'</table>'
        #return output
        self.mkTableHeaders(model)
        return model

    def mkTableHeaders(self, model):
        for i in range(len(self._tableHeaders)):
            model.setHeaderData(i, QtCore.Qt.Horizontal, self._tableHeaders[i])


    def copySelectionToClipboard(self):
        selection = self.ui.tableView.selectionModel() #self.table = QAbstractItemView
        indexes = selection.selectedIndexes()
        #print indexes

        columns = indexes[-1].column() - indexes[0].column() + 1
        rows = len(indexes) / columns
        textTable = [[""] * columns for i in xrange(rows)]

        model = self.ui.tableView.model()
        for i, index in enumerate(indexes):
            #print i, index, model.data(index).toString()
            textTable[i % rows][i / rows] = unicode(model.data(index).toString()) #self.model = QAbstractItemModel 
        #print textTable
        clipboardText = "\n".join(("\t".join(i) for i in textTable))
        QtGui.QApplication.clipboard().setText(clipboardText)

