# -*- coding: utf-8 -*-
import pymssql
import _mssql
import MySQLdb

SHOST = '10.0.0.5'
SUSER = 'wiffzack'
SPASSWORD = 'wiffzack'
SDATABASE = 'wiffzack'

THOST = 'localhost'
TUSER = 'root'
TPASSWORD = 'kiz2tl'
TDATABASE = 'lagerManager'

class DbImporter(object):

	def __init__(self):
		self.connectToDb()
		
		
	def connectToDb(self):
		self.sourceDb = pymssql.connect(host=SHOST,user=SUSER,password=SPASSWORD,database=SDATABASE)
		self.targetDb = MySQLdb.connect (host=THOST,user=TUSER,passwd=TPASSWORD,db=TDATABASE)
		
		
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
		
		
	def commit(self, db = None):
		print "commiting"
		if db is None:
			raise error
		db.commit()

	def rollback(self, db = None):
		print "rolling back"
		if db is None:
			raise error
		db.rollback()
		
		
		
	def import_(self):
		print "syncing"
		s = self.sourceDb
		t = self.targetDb
		
		##################
		#checkpoints
		##################
		print 'importing checkpoints'
		query = "select * from journal_checkpoints order by checkpoint_id"
		res = self.runQuery(query, db=s)
		
		for row in res:
			query = """insert into journal_checkpoints
					(checkpoint_id, checkpoint_typ, checkpoint_datum, checkpoint_anmerkung, checkpoint_info, checkpoint_num)
					values
					(%s, %s, %s, %s, %s, %s)""" 
			self.runQuery(query, (row[0], row[1], row[2], row[3], row[4], row[5]), t)
			
			
		##################
		#journal_daten
		##################
		print 'importing journal daten'
		query = "select * from journal_daten order by daten_rechnung_id"
		res = self.runQuery(query, db=s)
		
		for row in res:
			query = """insert into journal_daten
					(daten_rechnung_id, daten_checkpoint_tag, daten_checkpoint_monat, daten_checkpoint_jahr, daten_checkpoint_kellner)
					values
					(%s, %s, %s, %s, %s)"""
			self.runQuery(query, (row[0], row[1], row[2], row[3], row[4]), t)
			
			
		##################
		#journal_details
		##################
		print 'importing journal details'
		query = "select * from journal_details order by detail_id"
		res = self.runQuery(query, db=s)
		
		for row in res:
			query = """insert into journal_details (detail_id, detail_journal, detail_absmenge, detail_istUmsatz, detail_preis, detail_artikel_text, detail_mwst, detail_bonier_datum, detail_gruppe, detail_istRabatt, detail_rabatt, detail_kellner, detail_autoEintrag, detail_ep, detail_ep_mwst)
					values
					(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			self.runQuery(query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]), t)
		
#		self.commit(t)


		##################
		#artikel basis
		##################
		#print 'importing artikel basis'
		#query = """select artikel_id, artikel_bezeichnung, artikel_gruppe, artikel_ep, artikel_ep_mwst, artikel_preis_popup, artikel_ep_preis_popup, artikel_bemerkung, artikel_bezeichnung_2
					#from artikel_basis"""
		#res = self.runQuery(query, db=s)
		
		#for row in res:
			#query = "insert into artikel_basis (artikel_id, artikel_bezeichnung, artikel_gruppe, artikel_ep, artikel_ep_mwst, artikel_preis_popup, artikel_ep_preis_popup, artikel_bemerkung, artikel_bezeichnung_2) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
			#self.runQuery(query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]), t)

		
		
		###################
		##lager artikel
		###################
		#print 'importing lager artikel'
		#query = """select lager_artikel_lagerartikel, lager_artikel_lieferant, lager_artikel_lieferant_artikel, lager_artikel_artikel, lager_artikel_prioritaet, lager_artikel_einheit, lager_artikel_lager, lager_artikel_flags, lager_artikel_maxStand, lager_artikel_minStand
					#from lager_artikel
					#where 1=1"""
		#res = self.runQuery(query, db=s)
		
		#for row in res:
			#query = "insert into lager_artikel (lager_artikel_lagerartikel, lager_artikel_lieferant, lager_artikel_lieferant_artikel, lager_artikel_artikel, lager_artikel_prioritaet, lager_artikel_einheit, lager_artikel_lager, lager_artikel_flags, lager_artikel_maxStand, lager_artikel_minStand) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			#self.runQuery(query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]), t)
			
			
		###################
		##zutaten
		###################
		#print 'importing zutaten'
		#query = """select zutate_master_artikel, zutate_artikel, zutate_menge, zutate_istFixiert, zutate_istZutat, zutate_istRezept, zutate_immerAnzeigen, zutate_istZwangsAbfrage, zutate_preisVerwenden
				#from artikel_zutaten"""
		#res = self.runQuery(query, db=s)
		
		#for row in res:
			#query = "insert into artikel_zutaten (zutate_master_artikel, zutate_artikel, zutate_menge, zutate_istFixiert, zutate_istZutat, zutate_istRezept, zutate_immerAnzeigen, zutate_istZwangsAbfrage, zutate_preisVerwenden) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
			#self.runQuery(query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]), t)
			#"""
			
		self.commit(t)

if __name__ == "__main__":
	importer = DbImporter()
	importer.import_()
