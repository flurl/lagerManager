# -*- coding: utf-8 -*-
import pymssql
import _mssql
import MySQLdb 

def connectToSource():
	host = u'192.168.2.100'
	db = u'wiffzack'
	user = u'wiffzack'
	pw = u'wiffzack'
	con = pymssql.connect(host=host,user=user,password=pw,database=db,charset='cp1252')
	print "con:", con
	return con

def connectToTarget():
	host = u'10.0.0.101'
	db = u'lagerManager'
	user = u'lager_manager'
	pw = u'post1309'
	con = MySQLdb.connect(host,user,pw,db)
	print "con:", con
	return con

def runQuery(query, values = None, db = None):
		#print query, values
		if db is None:
			raise error
		cur = db.cursor()
		if values is None:
			cur.execute(query)
		else:
			cur.execute(query, values)
		return cur.fetchall()


sCon = connectToSource()
tCon = connectToTarget()


sQuery = "select detail_id, detail_preis from journal_details"
res = runQuery(sQuery, db=sCon)
for row in res:
	tQuery = "update journal_details set detail_preis = %s where detail_id = %s" %(float(row[1]), row[0])
	print "running query:", tQuery
	runQuery(tQuery, db=tCon)
	
tQuery = "COMMIT";
runQuery(tQuery, db=tCon)
