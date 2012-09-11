# -*- coding: utf-8 -*-
from PyQt4 import QtSql

from CONSTANTS import *

dbConn = QtSql.QSqlDatabase.addDatabase('QMYSQL')

def connect(host, user, pw, db):
	dbConn.setHostName(host)
	dbConn.setDatabaseName(db)
	dbConn.setPassword(pw)
	dbConn.setUserName(user)
	ok = dbConn.open()  
	if not ok:
		print 'Failed to open database'
		return False
	else:
		return True
