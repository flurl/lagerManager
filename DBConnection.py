# -*- coding: utf-8 -*-
from PyQt4 import QtSql

from CONSTANTS import *

dbConn = QtSql.QSqlDatabase.addDatabase('QMYSQL')
connName = ''

def connect(host, user, pw, db, name=''):
	global dbConn, connName
	dbConn.setHostName(host)
	dbConn.setDatabaseName(db)
	dbConn.setPassword(pw)
	dbConn.setUserName(user)
	ok = dbConn.open()  
	if not ok:
		print 'Failed to open database'
		return False
	else:
		connName = name
		return True
