# -*- coding: utf-8 -*-
from lib.LMBase import *

class ReportBase(LMBase):
    
    def __init__(self, parent):
        LMBase.__init__(self, parent)
        
    @property
    def cfgKey(self):
        return 'report_' + self.ident
    
    def updatePeriod(self, p):
        super(ReportBase, self).updatePeriod(p)
        self.updateData()
