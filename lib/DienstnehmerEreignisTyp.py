# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from lib.LMDatabaseObject import LMDatabaseObject
#from lib.LMDatabaseRelation import LMDatabaseRelation

class DienstnehmerEreignisTyp(LMDatabaseObject):

    _DBTable = 'dir_typen'
    #	_dynamicColumns = {'stundensatz':'getHourlyWage'}
#    dienstnehmer = LMDatabaseRelation('dir_dinid', 'lib.Dienstnehmer.Dienstnehmer')
#    typ = LMDatabaseRelation('dir_ditid', 'lib.DienstnehmerEreignisTyp.DienstnehmerEreignisTyp')

    def __unicode__(self):
        return unicode(self['dit_kbez'])
        
    def __str__(self):
        return unicode(self).encode('utf-8')


