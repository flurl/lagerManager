# -*- coding: utf-8 -*-
import time
import copy

from PyQt4 import QtCore, QtGui, QtSql

from ui.reports.minimumLagerstandReport_gui import Ui_MinimumLagerstand
from textReport import TextReport



class MinimumLagerstandReport(TextReport):
    ident = 'MinimumLagerstand'
    
    def __init__(self, parent=None):
        TextReport.__init__(self, parent)
        
        self.ui = Ui_MinimumLagerstand()
        self.ui.setupUi(self)
        
        self.setHeader('Testheader')
        self.setFooter('Testfooter')
        
        query = """
                select * from lager_artikel
                """
        
        self.setData(query)
        
        self.process()
        
#		self.connect(self.ui.pushButton_refresh, QtCore.SIGNAL('clicked()'), self._onRefreshBtnClicked)
#		self.connect(self.ui.lineEdit_filterArticles, QtCore.SIGNAL('textChanged (const QString&)'), self._onArticleFilterChanged)
        
#		self.updateData()
#		self.plot()
        
    
