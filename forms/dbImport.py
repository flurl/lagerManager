# -*- coding: utf-8 -*-
import sys

from PyQt4 import QtCore, QtGui, QtSql
import pymssql
import _mssql


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
				
			query.prepare('select ifnull(max(checkpoint_id), 0) from journal_checkpoints where checkpoint_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
			query.next()
			id_ = query.value(0).toInt()[0]
			
			"""if id_ == 0 and not checkpointId:
				q = "select ifnull(max(checkpoint_id), 0) from journal_checkpoints where checkpoint_typ = 3"
				res = self.runQuery(q, db=s)
				id_ = res[0][0]"""
			
			if checkpointId is None:
				q = "select * from journal_checkpoints where checkpoint_id > %s order by checkpoint_id" % (id_, )
			else:
				q = "select * from journal_checkpoints where checkpoint_id > %s and checkpoint_id <= %s order by checkpoint_id" % (id_, checkpointId)
			print q
			res = self.runQuery(q, db=s)
			
			for row in res:
				query.prepare("""insert into journal_checkpoints
						(checkpoint_id, checkpoint_typ, checkpoint_datum, checkpoint_anmerkung, checkpoint_info, checkpoint_num, checkpoint_periode)
						values
						(?, ?, ?, ?, ?, ?, ?)""") 
				query.bindValue(0, row[0])
				query.bindValue(1, row[1])
				query.bindValue(2, row[2])
				query.bindValue(3, row[3])
				query.bindValue(4, row[4])
				query.bindValue(5, row[5])
				query.bindValue(6, periodId)
				query.exec_()
				if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
				

			##################
			#journal_daten
			##################
			print 'importing journal daten'
			
			query = QtSql.QSqlQuery()
		
			print 'deleting'
			query = QtSql.QSqlQuery()
			query.prepare('delete from journal_daten where daten_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
				print 'Error in query:', query.lastError().text()
				
			query.prepare('select ifnull(max(daten_rechnung_id), 0) from journal_daten where daten_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
			query.next()
			id_ = query.value(0).toInt()[0]
			
			s = self.connectToSource()
			if checkpointId is None:
				q = "select * from journal_daten where daten_rechnung_id > %s order by daten_rechnung_id" % (id_, )
			else:
				q = "select * from journal_daten where daten_rechnung_id > %s and daten_checkpoint_jahr = %s order by daten_rechnung_id" % (id_, checkpointId)
			res = self.runQuery(q, db=s)
			
			for row in res:
				query.prepare("""insert into journal_daten
						(daten_rechnung_id, daten_checkpoint_tag, daten_checkpoint_monat, daten_checkpoint_jahr, daten_checkpoint_kellner, daten_periode)
						values
						(?, ?, ?, ?, ?, ?)""")
				query.bindValue(0, row[0])
				query.bindValue(1, row[1])
				query.bindValue(2, row[2])
				query.bindValue(3, row[3])
				query.bindValue(4, row[4])
				query.bindValue(5, periodId)
				query.exec_()
				if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
				
				
			##################
			#journal_details
			##################
			print 'importing journal details'
			
			query = QtSql.QSqlQuery()
		
			print 'deleting'
			query.prepare('delete from journal_details where detail_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
				print 'Error in query:', query.lastError().text()
			
			query.prepare('select ifnull(max(detail_id), 0) from journal_details where detail_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
			query.next()
			id_ = query.value(0).toInt()[0]
			
			s = self.connectToSource()
			if checkpointId is None:
				q = "select * from journal_details where detail_id > %s order by detail_id" %(id_, )
			else:
				q = """select * from journal_details, journal_daten 
						where 1=1
						and detail_id > %s 
						and daten_rechnung_id = detail_journal
						and daten_checkpoint_jahr = %s
						order by detail_id""" %(id_, checkpointId)
			res = self.runQuery(q, db=s)
			
			for row in res:
				query.prepare("""insert into journal_details (detail_id, detail_journal, detail_absmenge, detail_istUmsatz, detail_preis, detail_artikel_text, detail_mwst, detail_bonier_datum, detail_gruppe, detail_istRabatt, detail_rabatt, detail_kellner, detail_autoEintrag, detail_ep, detail_ep_mwst, detail_periode)
						values
						(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""")
				query.bindValue(0, row[0])
				query.bindValue(1, row[1])
				query.bindValue(2, row[2])
				query.bindValue(3, row[3])
				query.bindValue(4, float(row[4]))
				query.bindValue(5, row[5])
				query.bindValue(6, float(row[6]))
				query.bindValue(7, str(row[7]))
				query.bindValue(8, row[8])
				query.bindValue(9, row[9])
				query.bindValue(10, row[10])
				query.bindValue(11, row[11])
				query.bindValue(12, row[12])
				query.bindValue(13, row[13])
				query.bindValue(14, row[14])
				query.bindValue(15, periodId)
				query.exec_()
				if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
					
					
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
			
			query.prepare('select ifnull(max(rechnung_id), 0) from rechnungen_basis where rechnung_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
			query.next()
			id_ = query.value(0).toInt()[0]
			
			s = self.connectToSource()
			if checkpointId is None:
				q = "select * from rechnungen_basis where rechnung_id > %s order by rechnung_id" %(id_, )
			else:
				q = """select * from rechnungen_basis, journal_daten 
						where 1=1
						and rechnung_id > %s 
						and daten_rechnung_id = rechnung_id
						and daten_checkpoint_jahr = %s
						order by rechnung_id""" %(id_, checkpointId)
			res = self.runQuery(q, db=s)
			
			for row in res:
				query.prepare("""insert into rechnungen_basis (rechnung_id, rechnung_typ, rechnung_nr, rechnung_dt_erstellung, rechnung_kellnerKurzName, rechnung_tischCode, rechnung_tischBereich, rechnung_adresse, rechnung_istStorno, rechnung_retour, rechnung_dt_zusatz, rechnung_periode)
						values
						(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""")
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
				query.addBindValue(row[10])
				query.addBindValue(periodId)
				query.exec_()
				if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()

			

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
			
			query.prepare('select ifnull(max(artikel_id), 0) from artikel_basis where artikel_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			if query.lastError().isValid():
					print 'Error in query:', query.lastError().text()
			query.next()
			id_ = query.value(0).toInt()[0]
			
			s = self.connectToSource()
			q = """select artikel_id, artikel_bezeichnung, artikel_gruppe, isnull(artikel_ep, 0.0), artikel_ep_mwst, artikel_preis_popup, artikel_ep_preis_popup, artikel_bemerkung, artikel_bezeichnung_2
						from artikel_basis where artikel_id > %s""" % (id_, )
			res = self.runQuery(q, db=s)
			
			for row in res:
				query.prepare("insert into artikel_basis (artikel_id, artikel_bezeichnung, artikel_gruppe, artikel_ep, artikel_ep_mwst, artikel_preis_popup, artikel_ep_preis_popup, artikel_bemerkung, artikel_bezeichnung_2, artikel_periode) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
				query.addBindValue(row[0])
				query.addBindValue(row[1])
				query.addBindValue(row[2])
				query.addBindValue(float(row[3]))
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
		
