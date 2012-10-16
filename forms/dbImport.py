# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql
import pymssql
import _mssql


from forms.formBase import FormBase
from ui.forms.importForm_gui import Ui_ImportForm
import config

class ImportForm(FormBase):
	
	uiClass = Ui_ImportForm
	ident = 'dbImport'
	
	def setupUi(self):
		super(ImportForm, self).setupUi()
		try:
			c = config.config['form_'+self.ident]
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
		initialImport = self.ui.checkBox_initialImport.isChecked()
		
		self.beginTransaction()
		
		##################
		#checkpoints
		##################
		print 'importing checkpoints'
		
		query = QtSql.QSqlQuery()
		if initialImport:
			print 'deleting'
			query = QtSql.QSqlQuery()
			query.prepare('delete from journal_checkpoints where checkpoint_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			
		query.prepare('select ifnull(max(checkpoint_id), 0) from journal_checkpoints where checkpoint_periode = ?')
		query.addBindValue(periodId)
		query.exec_()
		query.next()
		id_ = query.value(0).toInt()[0]
		
		q = "select * from journal_checkpoints where checkpoint_id > %s order by checkpoint_id" % (id_, )
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
			

		##################
		#journal_daten
		##################
		print 'importing journal daten'
		
		query = QtSql.QSqlQuery()
		if initialImport:
			print 'deleting'
			query = QtSql.QSqlQuery()
			query.prepare('delete from journal_daten where daten_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
			
		query.prepare('select ifnull(max(daten_rechnung_id), 0) from journal_daten where daten_periode = ?')
		query.addBindValue(periodId)
		query.exec_()
		query.next()
		id_ = query.value(0).toInt()[0]
		
		s = self.connectToSource()
		q = "select * from journal_daten where daten_rechnung_id > %s order by daten_rechnung_id" % (id_, )
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
			
			
		##################
		#journal_details
		##################
		print 'importing journal details'
		
		query = QtSql.QSqlQuery()
		if initialImport:
			print 'deleting'
			query.prepare('delete from journal_details where detail_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
		
		query.prepare('select ifnull(max(detail_id), 0) from journal_details where detail_periode = ?')
		query.addBindValue(periodId)
		query.exec_()
		query.next()
		id_ = query.value(0).toInt()[0]
		
		s = self.connectToSource()
		q = "select * from journal_details where detail_id > %s order by detail_id" %(id_, )
		res = self.runQuery(q, db=s)
		
		for row in res:
			query.prepare("""insert into journal_details (detail_id, detail_journal, detail_absmenge, detail_istUmsatz, detail_preis, detail_artikel_text, detail_mwst, detail_bonier_datum, detail_gruppe, detail_istRabatt, detail_rabatt, detail_kellner, detail_autoEintrag, detail_ep, detail_ep_mwst, detail_periode)
					values
					(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""")
			query.bindValue(0, row[0])
			query.bindValue(1, row[1])
			query.bindValue(2, row[2])
			query.bindValue(3, row[3])
			query.bindValue(4, row[4])
			query.bindValue(5, row[5])
			query.bindValue(6, row[6])
			query.bindValue(7, row[7])
			query.bindValue(8, row[8])
			query.bindValue(9, row[9])
			query.bindValue(10, row[10])
			query.bindValue(11, row[11])
			query.bindValue(12, row[12])
			query.bindValue(13, row[13])
			query.bindValue(14, row[14])
			query.bindValue(15, periodId)
			query.exec_()

		

		##################
		#artikel basis
		##################
		print 'importing artikel basis'
		
		query = QtSql.QSqlQuery()
		if initialImport:
			print 'deleting'
			query.prepare('delete from artikel_basis where artikel_periode = ?')
			query.addBindValue(periodId)
			query.exec_()
		
		query.prepare('select ifnull(max(artikel_id), 0) from artikel_basis where artikel_periode = ?')
		query.addBindValue(periodId)
		query.exec_()
		query.next()
		id_ = query.value(0).toInt()[0]
		
		s = self.connectToSource()
		q = """select artikel_id, artikel_bezeichnung, artikel_gruppe, artikel_ep, artikel_ep_mwst, artikel_preis_popup, artikel_ep_preis_popup, artikel_bemerkung, artikel_bezeichnung_2
					from artikel_basis where artikel_id > %s""" % (id_, )
		res = self.runQuery(q, db=s)
		
		for row in res:
			query.prepare("insert into artikel_basis (artikel_id, artikel_bezeichnung, artikel_gruppe, artikel_ep, artikel_ep_mwst, artikel_preis_popup, artikel_ep_preis_popup, artikel_bemerkung, artikel_bezeichnung_2, artikel_periode) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
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
			
		
		
		##################
		#lager artikel
		##################
		print 'importing lager artikel'
		
		query = QtSql.QSqlQuery()
		print 'deleting'
		query.prepare('delete from lager_artikel where lager_artikel_periode = ?')
		query.addBindValue(periodId)
		query.exec_()
		
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
			
			
		##################
		#lager_einheiten
		##################
		print 'importing lager_einheiten'
		
		query = QtSql.QSqlQuery()
		print 'deleting'
		query.prepare('delete from lager_einheiten where lager_einheit_periode = ?')
		query.addBindValue(periodId)
		query.exec_()
		
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

			
		##################
		#zutaten
		##################
		print 'importing zutaten'
		
		query = QtSql.QSqlQuery()
		print 'deleting'
		query.prepare('delete from artikel_zutaten where zutate_periode = ?')
		query.addBindValue(periodId)
		query.exec_()
		
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
			
			
		self.commit()
		
		print 'finished'
		QtGui.QMessageBox.information(self, 'Import abgeschlossen', 'Import abgeschlossen')
		
		
	def closeEvent(self, event):
		host = unicode(self.ui.lineEdit_host.text())
		db = unicode(self.ui.lineEdit_database.text())
		user = unicode(self.ui.lineEdit_user.text())
		pw = unicode(self.ui.lineEdit_password.text())
		config.config['form_'+self.ident] = {'lastHost': host, 'lastDb': db, 'lastUser': user, 'lastPw': pw}
		config.config.write()
		event.accept()
		
