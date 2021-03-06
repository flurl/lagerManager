# -*- coding: utf-8 -*-
import sys
import datetime

from PyQt4 import QtCore, QtGui, QtSql
import pymssql
import _mssql
import MySQLdb as mysql

"""mysql.connect(host='10.0.0.101',
             user='lager_manager',
             passwd='post1309',
             db='lagerManager_test',
             charset='utf8',
             use_unicode=True)
"""

from forms.formBase import FormBase
from ui.forms.importForm_gui import Ui_ImportForm
import config
import DBConnection


class ImportForm(FormBase):
	
	uiClass = Ui_ImportForm
	ident = 'dbImport'
	
	def setupUi(self):
		super(ImportForm, self).setupUi()
		try:
			c = config.config[self.cfgKey]['connection'][DBConnection.connName]
			self.ui.lineEdit_host.setText(c['lastHost'])
			self.ui.lineEdit_database.setText(c['lastDb'])
			self.ui.lineEdit_user.setText(c['lastUser'])
			self.ui.lineEdit_password.setText(c['lastPw'])
		except KeyError:
			pass

	def setupSignals(self):
		super(ImportForm, self).setupSignals()
		self.connect(self.ui.pushButton_import, QtCore.SIGNAL('clicked()'), self.startImport)
		
	def connectToSource(self):
		host = unicode(self.ui.lineEdit_host.text())
		db = unicode(self.ui.lineEdit_database.text())
		user = unicode(self.ui.lineEdit_user.text())
		pw = unicode(self.ui.lineEdit_password.text())
		con = pymssql.connect(host=host,user=user,password=pw,database=db,charset='cp1252')
		print "con:", con
		return con
	
	def runQuery(self, query, values = None, db = None):
		#print query, values
		if db is None:
			raise error
		cur = db.cursor()
		if values is None:
			cur.execute(query)
		else:
			cur.execute(query, values)
		return cur.fetchall()
		
	def prepareValuesForSQLString(self, vals):
		#print vals
		tmp = []
		for v in vals:
			#print u"v: %s" % (v, ), type(v)
			if isinstance(v, basestring):
				tmp.append(unicode(mysql.escape_string(v.encode('utf-8')), 'utf-8'))
			elif v is None:
				tmp.append(u'NULL')
			elif isinstance(v, datetime.datetime):
				tmp.append(v.strftime('%Y-%m-%d %H:%M:%S'))
			elif isinstance(v, bool):
				tmp.append(int(v))
			else:
				tmp.append(v)
		#print tmp
		return tuple(tmp)
		
		
	def insertMultipleValues(self, insertStr, valuesStr, vals, additionalVals=None):
		query = QtSql.QSqlQuery()
		i = 0
		values = []
		for row in vals:
			values.append(valuesStr % self.prepareValuesForSQLString(row+additionalVals))
			i += 1
			
			if i == 1000:
				print "got 1000"
				sql = insertStr + ",".join(values)
				query.prepare(sql)
				query.exec_()
				if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
				i = 0
				values = []
			
		if (len(values) > 0):
			sql = insertStr + ",".join(values)
			query.prepare(sql)
			query.exec_()
			if query.lastError().isValid():
				print 'Error in query:', query.lastError().text()
		
		
	def startImport(self):
		print "syncing"
		s = self.connectToSource()
		periodId = self.getCurrentPeriodId()
		checkpointId = self.getCheckpointIdForPeriod(periodId)
		
		try:
			
			query = QtSql.QSqlQuery()
			query.prepare('SET foreign_key_checks = 0')
			query.exec_()
			if query.lastError().isValid():
				print 'Error in query:', query.lastError().text()
			
			
			self.beginTransaction()
			
			##################
			#checkpoints
			##################
			print 'importing checkpoints'
			
			query = QtSql.QSqlQuery()
		
			print 'deleting'
			query = QtSql.QSqlQuery()
			query.prepare('delete from journal_checkpoints where checkpoint_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
				print 'Error in query:', query.lastError().text()
			
			q = "select * from journal_checkpoints order by checkpoint_id"
			print q
			res = self.runQuery(q, db=s)
			
			for row in res:
				query.prepare("""insert into journal_checkpoints
						(checkpoint_id, checkpoint_typ, checkpoint_datum, checkpoint_anmerkung, checkpoint_info, checkpoint_num, checkpoint_kassenbuch_verarbeitet, checkpoint_periode)
						values
						(?, ?, ?, ?, ?, ?, ?, ?)""") 
				query.bindValue(0, row[0])
				query.bindValue(1, row[1])
				query.bindValue(2, row[2])
				query.bindValue(3, row[3])
				query.bindValue(4, row[4])
				query.bindValue(5, row[5])
				query.bindValue(6, row[6])
				query.bindValue(7, periodId)
				query.exec_()
				if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
				

			##################
			#tische_aktiv
			##################
			print 'importing tische_aktiv'
			
			query = QtSql.QSqlQuery()
		
			print 'deleting'
			query = QtSql.QSqlQuery()
			query.prepare('delete from tische_aktiv where tisch_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
				print 'Error in query:', query.lastError().text()
			
			s = self.connectToSource()
			q = "select * from tische_aktiv where checkpoint_jahr %s order by tisch_id" % ("="+str(self.getCheckpointIdForPeriod(periodId)) if self.getCheckpointIdForPeriod(periodId) is not None else "is null")
			res = self.runQuery(q, db=s)
			
			insertStr = """insert into tische_aktiv
						(tisch_id, tisch_bereich, tisch_pri_nummer, tisch_sek_nummer, tisch_gast,
						tisch_dt_erstellung, tisch_dt_aktivitaet, tisch_kellner, tisch_fertig,
						tisch_zahlungsart, tisch_rechnung, tisch_dt_zusatz, tisch_adresse, tisch_kellner_abrechnung,
						tisch_client, tisch_reservierung, tisch_reservierung_check, tisch_zusatz_text,
						checkpoint_tag, checkpoint_monat, checkpoint_jahr, tisch_externer_beleg, tisch_periode)
						values """
			valuesStr = "(%s, %s, %s, %s, %s, '%s', '%s', %s, %s, %s, %s, '%s', %s, %s, '%s', %s, %s, '%s', %s, %s, %s, %s, %s)"
			self.insertMultipleValues(insertStr, valuesStr, res, (periodId, ))
			
			
			##################
			#tische_bons
			##################
			print 'importing tische_bons'
			
			query = QtSql.QSqlQuery()
		
			print 'deleting'
			query.prepare('delete from tische_bons where tisch_bon_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
				print 'Error in query:', query.lastError().text()
			
			s = self.connectToSource()
			q = "select tisch_bon_id, tisch_bon_dt_erstellung, tisch_bon_tisch, tisch_bon_kellner, tisch_bon_client, tisch_bon_typ, tisch_bon_bestellkarte, tisch_bon_vorgangsart from tische_bons, tische_aktiv where tisch_bon_tisch = tisch_id and tische_aktiv.checkpoint_jahr %s order by tisch_bon_id" % ("="+str(self.getCheckpointIdForPeriod(periodId)) if self.getCheckpointIdForPeriod(periodId) is not None else "is null")
			res = self.runQuery(q, db=s)
			
			insertStr = """insert into tische_bons 
								(tisch_bon_id, tisch_bon_dt_erstellung, tisch_bon_tisch, tisch_bon_kellner,
								tisch_bon_client, tisch_bon_typ, tisch_bon_bestellkarte, tisch_bon_vorgangsart,
								tisch_bon_periode)
								values """
			valuesStr = "(%s, '%s', %s, %s, '%s', %s, %s, %s, %s)"
			self.insertMultipleValues(insertStr, valuesStr, res, (periodId, ))


			##################
			#tische_bondetails
			##################
			print 'importing tische_bondetails'
			
			query = QtSql.QSqlQuery()
		
			print 'deleting'
			query.prepare('delete from tische_bondetails where tisch_bondetail_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
				print 'Error in query:', query.lastError().text()
			
			s = self.connectToSource()
			q = "select tisch_bondetail_id, tisch_bondetail_bon, tisch_bondetail_master_id, tisch_bondetail_menge, \
								tisch_bondetail_absmenge, tisch_bondetail_istUmsatz, tisch_bondetail_artikel, tisch_bondetail_preis, \
								tisch_bondetail_text, tisch_bondetail_mwst, tisch_bondetail_gangfolge, tisch_bondetail_hatRabatt, \
								tisch_bondetail_istRabatt, tisch_bondetail_autoEintrag, tisch_bondetail_stornoFaehig, tisch_bondetail_ep, \
								tisch_bondetail_ep_mwst, tisch_bondetail_preisgruppe, tisch_bondetail_gutschein_log, journal_preisgruppe, \
								journal_gruppe, journal_mwst, tisch_bondetail_istExternerBeleg from tische_bondetails, tische_bons, tische_aktiv where tisch_bondetail_bon = tisch_bon_id and tisch_bon_tisch = tisch_id and tische_aktiv.checkpoint_jahr %s order by tisch_bondetail_id" % ("="+str(self.getCheckpointIdForPeriod(periodId)) if self.getCheckpointIdForPeriod(periodId) is not None else "is null")
			res = self.runQuery(q, db=s)
			
			insertStr = u"""insert into tische_bondetails 
								(tisch_bondetail_id, tisch_bondetail_bon, tisch_bondetail_master_id, tisch_bondetail_menge,
								tisch_bondetail_absmenge, tisch_bondetail_istUmsatz, tisch_bondetail_artikel, tisch_bondetail_preis,
								tisch_bondetail_text, tisch_bondetail_mwst, tisch_bondetail_gangfolge, tisch_bondetail_hatRabatt,
								tisch_bondetail_istRabatt, tisch_bondetail_autoEintrag, tisch_bondetail_stornoFaehig, tisch_bondetail_ep,
								tisch_bondetail_ep_mwst, tisch_bondetail_preisgruppe, tisch_bondetail_gutschein_log, journal_preisgruppe,
								journal_gruppe, journal_mwst, tisch_bondetail_istExternerBeleg, tisch_bondetail_periode)
								values """
			valuesStr = u"(%s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', '%s', %s, %s, %s)"
			self.insertMultipleValues(insertStr, valuesStr, res, (periodId, ))
			
			
			##################
			#tische_bereiche
			##################
			print 'importing tische_bereiche'
			
			query = QtSql.QSqlQuery()
		
			print 'deleting'
			query.prepare('delete from tische_bereiche where tischbereich_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
				print 'Error in query:', query.lastError().text()
			
			s = self.connectToSource()
			q = "select * from tische_bereiche"
			res = self.runQuery(q, db=s)
			
			insertStr = u"""insert into tische_bereiche (tischbereich_id, tischbereich_kurzName, tischbereich_name, tischbereich_istGastBereich, tischbereich_minNummer, tischbereich_maxNummer, tischbereich_istAufwand, tischbereich_istSammelbereich, tischbereich_benoetigtAdresse, tischbereich_rechnungsAnzahl, tischbereich_extern, tischbereich_istOrdercardBereich, tischbereich_vorgangsart, tischbereich_temp, tischbereich_versteckeSammeltisch, tischbereich_sammeltischOptional, tischbereich_rksv, tischbereich_periode)
						values """
			valuesStr = u"(%s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			self.insertMultipleValues(insertStr, valuesStr, res, (periodId, ))
			
			
			##################
			#rechnungen_basis
			##################
			print 'importing rechnungen'
			
			query = QtSql.QSqlQuery()
		
			print 'deleting'
			query.prepare('delete from rechnungen_basis where rechnung_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
				print 'Error in query:', query.lastError().text()
			
			s = self.connectToSource()
			q = "select * from rechnungen_basis where checkpoint_jahr %s order by rechnung_id" % ("="+str(self.getCheckpointIdForPeriod(periodId)) if self.getCheckpointIdForPeriod(periodId) is not None else "is null")
			res = self.runQuery(q, db=s)
			
			insertStr = """insert into rechnungen_basis (rechnung_id, rechnung_typ, rechnung_nr, rechnung_dt_erstellung, rechnung_kellnerKurzName, rechnung_tischCode, rechnung_tischBereich, 
			rechnung_adresse, rechnung_istStorno, rechnung_retour, rechnung_dt_zusatz, checkpoint_tag, checkpoint_monat, checkpoint_jahr, 
			rechnung_kassenidentifikation, rechnung_barumsatz_nr, rechnung_gesamt_umsatz, rechnung_zertifikat_id, rechnung_referenz, rechnung_signatur, rechnung_druckpfad, rechnung_mwst_normal, 
			rechnung_mwst_ermaessigt1, rechnung_mwst_ermaessigt2, rechnung_mwst_null, rechnung_mwst_besonders, rechnung_gesamt_umsatz_enc, rechnung_rka, rechnung_vorherige_signatur, 
			rechnung_beleg_kennzeichen, rechnung_istTrainingsBeleg, rechnung_periode)
						values """
			valuesStr = "(%s, %s, %s, '%s', '%s', '%s', '%s', %s, %s, %s, '%s', %s, %s, %s, '%s', %s, %s, '%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s', '%s', '%s', '%s', %s, %s)"
			self.insertMultipleValues(insertStr, valuesStr, res, (periodId, ))
			
			
			##################
			#rechnungen_details
			##################
			print 'importing rechnungen_details'
			
			query = QtSql.QSqlQuery()
		
			print 'deleting'
			query.prepare('delete from rechnungen_details where rechnung_detail_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
				print 'Error in query:', query.lastError().text()
			
			s = self.connectToSource()
			q = "select rechnung_detail_id, rechnung_detail_rechnung, rechnung_detail_master_detail, rechnung_detail_menge, rechnung_detail_absmenge, rechnung_detail_text, rechnung_detail_mwst, rechnung_detail_preis, rechnung_detail_artikel_gruppe, rechnung_detail_text_2, rechnung_detail_bonierdatum from rechnungen_details, rechnungen_basis where rechnung_detail_rechnung = rechnung_id and rechnungen_basis.checkpoint_jahr %s order by rechnung_detail_id" % ("="+str(self.getCheckpointIdForPeriod(periodId)) if self.getCheckpointIdForPeriod(periodId) is not None else "is null")
			res = self.runQuery(q, db=s)
			
			insertStr = """insert into rechnungen_details (rechnung_detail_id, rechnung_detail_rechnung, rechnung_detail_master_detail, rechnung_detail_menge, rechnung_detail_absmenge, rechnung_detail_text, rechnung_detail_mwst, rechnung_detail_preis, rechnung_detail_artikel_gruppe, rechnung_detail_text_2, rechnung_detail_bonierdatum, rechnung_detail_periode)
						values """
			valuesStr = "(%s, %s, %s, %s, %s, '%s', %s, %s, '%s', '%s', '%s', %s)"
			self.insertMultipleValues(insertStr, valuesStr, res, (periodId, ))
			
			
			##################
			#artikel basis
			##################
			print 'importing artikel basis'
			
			query = QtSql.QSqlQuery()
			
			print 'deleting'
			query.prepare('delete from artikel_basis where artikel_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
				print 'Error in query:', query.lastError().text()
			
			s = self.connectToSource()
			q = """select artikel_id, artikel_bezeichnung, artikel_gruppe, isnull(artikel_ep, 0.0), artikel_ep_mwst, artikel_preis_popup, artikel_ep_preis_popup, artikel_bemerkung, artikel_bezeichnung_2, artikel_rksv, artikel_externer_beleg
						from artikel_basis"""
			res = self.runQuery(q, db=s)
			
			for row in res:
				query.prepare("insert into artikel_basis (artikel_id, artikel_bezeichnung, artikel_gruppe, artikel_ep, artikel_ep_mwst, artikel_preis_popup, artikel_ep_preis_popup, artikel_bemerkung, artikel_bezeichnung_2, artikel_rksv, artikel_externer_beleg, artikel_periode) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
				query.addBindValue(row[0])
				query.addBindValue(row[1])
				query.addBindValue(row[2])
				query.addBindValue(float(row[3]))
				query.addBindValue(row[4])
				query.addBindValue(row[5])
				query.addBindValue(row[6])
				query.addBindValue(row[7])
				query.addBindValue(row[8])
				query.addBindValue(row[9])
				query.addBindValue(row[10])
				query.addBindValue(periodId)
				query.exec_()
				if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
				
			
			
			##################
			#lager artikel
			##################
			print 'importing lager artikel'
			
			query = QtSql.QSqlQuery()
			print 'deleting'
			query.prepare('delete from lager_artikel where lager_artikel_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
			
			s = self.connectToSource()
			q = """select lager_artikel_lagerartikel, lager_artikel_lieferant, lager_artikel_lieferant_artikel, lager_artikel_artikel, lager_artikel_prioritaet, lager_artikel_einheit, lager_artikel_lager, lager_artikel_flags, lager_artikel_maxStand, lager_artikel_minStand
						from lager_artikel
						where 1=1"""
			res = self.runQuery(q, db=s)
			
			for row in res:
				query.prepare("insert into lager_artikel (lager_artikel_lagerartikel, lager_artikel_lieferant, lager_artikel_lieferant_artikel, lager_artikel_artikel, lager_artikel_prioritaet, lager_artikel_einheit, lager_artikel_lager, lager_artikel_flags, lager_artikel_maxStand, lager_artikel_minStand, lager_artikel_periode) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
				query.addBindValue(row[0])
				query.addBindValue(row[1])
				query.addBindValue(row[2])
				query.addBindValue(row[3])
				query.addBindValue(row[4])
				query.addBindValue(row[5])
				query.addBindValue(row[6])
				query.addBindValue(row[7])
				query.addBindValue(row[8])
				query.addBindValue(row[9])
				query.addBindValue(periodId)
				query.exec_()
				if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
				
				
			##################
			#lager_einheiten
			##################
			print 'importing lager_einheiten'
			
			query = QtSql.QSqlQuery()
			print 'deleting'
			query.prepare('delete from lager_einheiten where lager_einheit_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
			
			s = self.connectToSource()
			q = """select lager_einheit_id, lager_einheit_name, lager_einheit_multiplizierer, lager_einheit_basis
					from lager_einheiten"""
			res = self.runQuery(q, db=s)
			
			for row in res:
				query.prepare("insert into lager_einheiten (lager_einheit_id, lager_einheit_name, lager_einheit_multiplizierer, lager_einheit_basis, lager_einheit_periode) values (?, ?, ?, ?, ?)")
				query.addBindValue(row[0])
				query.addBindValue(row[1])
				query.addBindValue(row[2])
				query.addBindValue(row[3])
				query.addBindValue(periodId)
				query.exec_()
				if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
					
					
			##################
			#artikel_gruppen
			##################
			print 'importing artikel_gruppen'
			
			query = QtSql.QSqlQuery()
			print 'deleting'
			query.prepare('delete from artikel_gruppen where artikel_gruppe_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
			
			s = self.connectToSource()
			q = """	select artikel_gruppe_id, artikel_gruppe_parent_id, artikel_gruppe_name, artikel_gruppe_standard_gangfolge, 
					artikel_gruppe_bontyp, artikel_gruppe_istUmsatz, artikel_gruppe_zeigeAufRechnung, artikel_gruppe_druckeRezeptur,
					artikel_gruppe_keinStorno
					from artikel_gruppen"""
			res = self.runQuery(q, db=s)
			
			for row in res:
				query.prepare("insert into artikel_gruppen (artikel_gruppe_id, artikel_gruppe_parent_id, artikel_gruppe_name, artikel_gruppe_standard_gangfolge, artikel_gruppe_bontyp, artikel_gruppe_istUmsatz, artikel_gruppe_zeigeAufRechnung, artikel_gruppe_druckeRezeptur, artikel_gruppe_keinStorno, artikel_gruppe_periode) values (?, ?, ?, ?, ?,?, ?, ?, ?, ?)")
				query.addBindValue(row[0])
				query.addBindValue(row[1])
				query.addBindValue(row[2])
				query.addBindValue(row[3])
				query.addBindValue(row[4])
				query.addBindValue(row[5])
				query.addBindValue(row[6])
				query.addBindValue(row[7])
				query.addBindValue(row[8])
				query.addBindValue(periodId)
				query.exec_()
				if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()

				
			##################
			#zutaten
			##################
			print 'importing zutaten'
			
			query = QtSql.QSqlQuery()
			print 'deleting'
			query.prepare('delete from artikel_zutaten where zutate_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
			
			s = self.connectToSource()
			q = """select zutate_master_artikel, zutate_artikel, zutate_menge, zutate_istFixiert, zutate_istZutat, zutate_istRezept, zutate_immerAnzeigen, zutate_istZwangsAbfrage, zutate_preisVerwenden
					from artikel_zutaten"""
			res = self.runQuery(q, db=s)
			
			for row in res:
				query.prepare("insert into artikel_zutaten (zutate_master_artikel, zutate_artikel, zutate_menge, zutate_istFixiert, zutate_istZutat, zutate_istRezept, zutate_immerAnzeigen, zutate_istZwangsAbfrage, zutate_preisVerwenden, zutate_periode) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
				query.addBindValue(row[0])
				query.addBindValue(row[1])
				query.addBindValue(row[2])
				query.addBindValue(row[3])
				query.addBindValue(row[4])
				query.addBindValue(row[5])
				query.addBindValue(row[6])
				query.addBindValue(row[7])
				query.addBindValue(row[8])
				query.addBindValue(periodId)
				query.exec_()
				if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
					
					
			##################
			#mwst gruppen
			##################
			print 'importing mwst gruppen'
			
			query = QtSql.QSqlQuery()
			print 'deleting'
			query.prepare('delete from meta_mwstgruppen where mwst_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
			
			s = self.connectToSource()
			q = """select mwst_id, mwst_satz, mwst_bezeichnung
						from meta_mwstgruppen
						where 1=1"""
			res = self.runQuery(q, db=s)
			
			for row in res:
				query.prepare("insert into meta_mwstgruppen (mwst_id, mwst_satz, mwst_bezeichnung, mwst_periode) values (?, ?, ?, ?)")
				query.addBindValue(row[0])
				query.addBindValue(float(row[1]))
				query.addBindValue(row[2])
				query.addBindValue(periodId)
				query.exec_()
				if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
					
					
					
			##################
			#kellner_basis
			##################
			print 'importing kellner_basis'
			
			query = QtSql.QSqlQuery()
			print 'deleting'
			query.prepare('delete from kellner_basis where kellner_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
			
			s = self.connectToSource()
			q = """select * from kellner_basis
						where 1=1"""
			res = self.runQuery(q, db=s)
			
			for row in res:
				query.prepare("""insert into kellner_basis (
								kellner_id,	kellner_kurzName, kellner_uid, kellner_person, kellner_lager, kellner_schnellTisch_bereich,
								kellner_schnellTisch_pri_nummer, kellner_schnellTisch_sek_nummer, kellner_zeigeAuswahl, kellner_kasse,
								kellner_periode) 
								values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""")
				query.addBindValue(row[0])
				query.addBindValue(row[1])
				query.addBindValue(row[2])
				query.addBindValue(row[3])
				query.addBindValue(row[4])
				query.addBindValue(row[5])
				query.addBindValue(row[6])
				query.addBindValue(row[7])
				query.addBindValue(row[8])
				query.addBindValue(row[9])
				query.addBindValue(periodId)
				query.exec_()
				if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
				
				
			self.commit()
		
		except Exception, e:
			print "Import not successfull - rolling back", e
			self.rollback()
		
		finally:
			query = QtSql.QSqlQuery()
			query.prepare('SET foreign_key_checks = 1')
			query.exec_()
			if query.lastError().isValid():
				print 'Error in query:', query.lastError().text()
		
		print 'finished'
		QtGui.QMessageBox.information(self, 'Import abgeschlossen', 'Import abgeschlossen')
		
		
	def closeEvent(self, event):
		host = unicode(self.ui.lineEdit_host.text())
		db = unicode(self.ui.lineEdit_database.text())
		user = unicode(self.ui.lineEdit_user.text())
		pw = unicode(self.ui.lineEdit_password.text())
	
		cfgKey = self.cfgKey
	
		try:
			tmp = config.config[cfgKey]
		except KeyError:
			config.config[cfgKey] = {}
			
		try:
			tmp = config.config[cfgKey]['connection']
		except KeyError:
			config.config[cfgKey]['connection'] = {}
	
		config.config[cfgKey]['connection'][DBConnection.connName] = {'lastHost': host, 'lastDb': db, 'lastUser': user, 'lastPw': pw}
		config.config.write()
		super(ImportForm, self).closeEvent(event)
		
