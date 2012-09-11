# -*- coding: utf-8 -*-
import pymssql
import _mssql
import sqlite3
import decimal
import datetime
import time
import os
import sys
import random
import ConfigParser
import pickle
import getopt

from PyQt4 import QtCore, QtGui

from ui.statsMainWindow_gui import Ui_MainWindow
from articleSelectionDialog import ArticleSelectionDialog
from CONSTANTS import *

import GLOBALS


LEGENDWIDTH = 300
INFOPOPUPWIDTH = 200
INFOPOPUPHEIGHT = 50
INFOPOPUPSPACING = 15


sqlite3.register_adapter(decimal.Decimal, lambda x:float(x))
sqlite3.register_converter('decimal', decimal.Decimal)


class Rect(QtGui.QGraphicsRectItem):
	Type = QtGui.QGraphicsRectItem.UserType + 1

	def __init__(self, *args):
		QtGui.QGraphicsRectItem.__init__(self, *args)
		
		self._showInfo = False

		#self.graph = graphWidget
		#self.edgeList = []
		#self.newPos = QtCore.QPointF()
		#self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
		#self.setZValue(1)

	def type(self):
		return Rect.Type



	def paint(self, painter, option, widget):
		QtGui.QGraphicsRectItem.paint(self, painter, option, widget)

		if self._showInfo:			
			gvMatrix = self.scene().views()[0].matrix()
			currScaling = (1/gvMatrix.m11(), 1/gvMatrix.m22())
		
			f = QtGui.QFont("sans-serif", 10*currScaling[0], QtGui.QFont.Normal);
			painter.setFont(f)
		
			painter.setBrush(QtCore.Qt.gray)
			x, y = self.rect().x(), self.rect().y()
			painter.drawRect(x+INFOPOPUPSPACING, y, INFOPOPUPWIDTH*currScaling[0], INFOPOPUPHEIGHT*currScaling[1])
			
			painter.setPen(QtGui.QPen(QtGui.QColor(0,0,0)))
			y += 15*currScaling[1]
			painter.drawText(x+20, y, "Date: " + self.data(2).toString())
			y += 15*currScaling[1]
			painter.drawText(x+20, y, "Name: " + self.data(0).toString())
			y += 15*currScaling[1]
			painter.drawText(x+20, y, "Value: " + self.data(1).toString())
			#gradient = QtGui.QRadialGradient(-3, -3, 10)
			#if option.state & QtGui.QStyle.State_Sunken:
				#gradient.setCenter(3, 3)
				#gradient.setFocalPoint(3, 3)
				#gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.yellow).light(120))
				#gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkYellow).light(120))
			#else:
				#gradient.setColorAt(0, QtCore.Qt.yellow)
				#gradient.setColorAt(1, QtCore.Qt.darkYellow)
	
			#painter.setBrush(QtGui.QBrush(gradient))
			#painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
			#painter.drawEllipse(-10, -10, 20, 20)


	def hoverEnterEvent(self, event):
		self._showInfo = True
		self.update()



	def hoverLeaveEvent(self, event):
		self._showInfo = False
		self.update()
		
		
	
	def boundingRect(self):
		try:
			gvMatrix = self.scene().views()[0].matrix()
			currScaling = (1/gvMatrix.m11(), 1/gvMatrix.m22())
		except IndexError:
			currScaling = (1.0, 1.0)			
	
		rect = QtGui.QGraphicsRectItem.boundingRect(self)
		return QtCore.QRectF(rect.x(), rect.y(), rect.width()+INFOPOPUPWIDTH*currScaling[0]+INFOPOPUPSPACING, rect.height()+INFOPOPUPHEIGHT*currScaling[1])









class MainWindow(QtGui.QMainWindow):
	
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		
		self.colors = {}   # colors for the articles
		self.checkpoints = {}
		self.activeArticles = None
		
		self.ui = Ui_MainWindow()

		self.ui.setupUi(self)		
		
		self.loadConf()
		
		self._connectToDb()
		
		self._setupForm()
		
		self._drawChart()
		
		#self.connect(self.ui.pushButton_cancel, QtCore.SIGNAL('clicked()'), self._resetForm)
		
	
	
	def _setupForm(self):
		self._setupTimeFrameWidgets()
		self.connect(self.ui.pushButton_start, QtCore.SIGNAL('clicked()'), self._onStartBtnClicked)
		self.connect(self.ui.pushButton_zoomIn, QtCore.SIGNAL('clicked()'), self._onZoomInBtnClicked)
		self.connect(self.ui.pushButton_zoomOut, QtCore.SIGNAL('clicked()'), self._onZoomOutBtnClicked)
		self.connect(self.ui.pushButton_articles, QtCore.SIGNAL('clicked()'), self._onArticlesBtnClicked)
		self.connect(self.ui.pushButton_export, QtCore.SIGNAL('clicked()'), self._onExportBtnClicked)
		self.connect(self.ui.pushButton_syncDB, QtCore.SIGNAL('clicked()'), self._onSyncBtnClicked)
		self.connect(self.ui.pushButton_importArticles, QtCore.SIGNAL('clicked()'), self._onImportArticlesBtnClicked)
#		self.connect(self.ui.radioButton_revenues, QtCore.SIGNAL('clicked()'), self.plot)
#		self.connect(self.ui.radioButton_quantity, QtCore.SIGNAL('clicked()'), self.plot)
#		self.connect(self.ui.radioButton_consumption, QtCore.SIGNAL('clicked()'), self.plot)
		
		for i in range(0, 7):
			self.connect(getattr(self.ui, "checkBox_weekday%s" % i), QtCore.SIGNAL('clicked()'), self.plot)
				
		
	
	def _setupTimeFrameWidgets(self):
		"""set start and end date to first and last entry in database"""
		
		query = "select checkpoint_id, CAST([checkpoint_info] AS VARCHAR(8000)) \
				from journal_checkpoints \
				where 1=1 \
				and checkpoint_typ = 1 \
				order by checkpoint_datum desc"
		if DATABASE == 'wiffzack_backup':
			query = "select top 11 checkpoint_id, CAST([checkpoint_info] AS VARCHAR(8000)) \
				from journal_checkpoints \
				where 1=1 \
				and checkpoint_typ = 1 \
				order by checkpoint_datum desc"
		
		results = self._runQuery(query)
		
		for res in results:
			self.ui.comboBox_start.addItem(res[1], QtCore.QVariant(int(res[0])))
			self.ui.comboBox_end.addItem(res[1], QtCore.QVariant(int(res[0])))
		
			
		
	def _onStartBtnClicked(self):
		self._drawChart()
			
	
	
	def _onZoomInBtnClicked(self):
		self.ui.graphicsView_stats.scale(ZOOMINFACTOR, ZOOMINFACTOR)
		
		
		
	def _onZoomOutBtnClicked(self):
		self.ui.graphicsView_stats.scale(ZOOMOUTFACTOR, ZOOMOUTFACTOR)
		
	
	
	def _onArticlesBtnClicked(self):
		dlg = ArticleSelectionDialog(self)
		if dlg.show():
			pass
			
			
	def _onExportBtnClicked(self):
		
		#build default filename
		filename = self.ui.comboBox_start.currentText() + '-' + self.ui.comboBox_end.currentText() + '.csv'
	
		filename = QtGui.QFileDialog.getSaveFileName(self, self.tr('Save File'), filename)
		
		if filename != '':
	
			import CSVExporter
#			articles = self.checkpoints[self.checkpoints.keys()[0]]['articles']
			exp = CSVExporter.CSVExporter(self.checkpoints)

			self.setCursor(QtCore.Qt.WaitCursor)
			exp.export(filename)
			self.setCursor(QtCore.Qt.ArrowCursor)       
		
			ret = QtGui.QMessageBox.information(self, self.tr("Wiffzack Stats"),
		               self.tr("Export successfull"),
		               QtGui.QMessageBox.Ok);
                   

	def _onSyncBtnClicked(self):
		print "syncing"
		query = "select * from journal_checkpoints order by checkpoint_id"
		res = self._runQuery(query)
		
		for row in res:
			query = """insert into journal_checkpoints
					(checkpoint_id, checkpoint_typ, checkpoint_datum, checkpoint_anmerkung, checkpoint_info, checkpoint_num, checkpoint_kassenbuch_verarbeitet)
					values
					(?, ?, ?, ?, ?, ?, ?)""" 
			self._runQuery(query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6]), self._sqliteDb)
			
			
		query = "select * from journal_daten order by daten_rechnung_id"
		res = self._runQuery(query)
		
		for row in res:
			query = """insert into journal_daten
					(daten_rechnung_id, daten_checkpoint_tag, daten_checkpoint_monat, daten_checkpoint_jahr, daten_checkpoint_kellner)
					values
					(?, ?, ?, ?, ?)"""
			self._runQuery(query, (row[0], row[1], row[2], row[3], row[4]), self._sqliteDb)
			
			
		query = "select * from journal_details order by detail_id"
		res = self._runQuery(query)
		
		for row in res:
			query = """insert into journal_details (detail_id, detail_journal, detail_absmenge, detail_istUmsatz, detail_preis, detail_artikel_text, detail_mwst, detail_bonier_datum, detail_gruppe, detail_istRabatt, detail_rabatt, detail_kellner, detail_autoEintrag, detail_ep, detail_ep_mwst)
					values
					(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
			self._runQuery(query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]), self._sqliteDb)
		
		self._commit(self._sqliteDb)
		

	def _onImportArticlesBtnClicked(self):
		query = """select artikel_id, artikel_bezeichnung
					from artikel_basis, lager_artikel
					where 1=1
					and lager_artikel_artikel = artikel_id"""
		res = self._runQuery(query)
		
		for row in res:
			query = "insert into lager_artikel (artikel_id, artikel_bezeichnung) values (?, ?)"
			self._runQuery(query, (row[0], row[1]), self._sqliteDb)
			
		self._commit(self._sqliteDb)

		
		
		
	def closeEvent(self, e):
		self._closeApp()
		
		
	def keyPressEvent(self, event):
		if (event.key() == QtCore.Qt.Key_Control):
			GLOBALS.keyCtrlPressed = True

		
	def keyReleaseEvent(self, event):
		if (event.key() == QtCore.Qt.Key_Control):
			GLOBALS.keyCtrlPressed = False
		
		
	def _closeApp(self):
		self.saveConf()
		self.close()
		
		
	
	def _getWeekdayList(self):
		weekdays = []
		for i in range(0, 7):
			if getattr(self.ui, "checkBox_weekday%s" % i).isChecked(): weekdays.append(i)
		return weekdays
		
		
		
	def _setWeekdays(self, days):
		for d in days:
			getattr(self.ui, "checkBox_weekday%s" % d).setCheckState(QtCore.Qt.Checked)
		
		
		
	def _connectToDb(self):
		self._dbCon = pymssql.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE)
		#self._dbCon = pymssql.connect(server='192.168.2.100',user=USER,password=PASSWORD,database=DATABASE)
		#self._dbCon = pymssql.connect('192.168.2.100:1433', USER, PASSWORD)
		self._sqliteDb = sqlite3.connect(SQLITEDB)
		
		
		
	def _runQuery(self, query, values = None, db = None):
		#print query, values
		if db is None:
			db = self._dbCon
		cur = db.cursor()
		if values is None:
			cur.execute(query)
		else:
			cur.execute(query, values)
		return cur.fetchall()
		
		
	def _commit(self, db = None):
		print "commiting"
		if db is None:
			db = self._dbCon
		db.commit()

	def _rollback(self, db = None):
		print "rolling back"
		if db is None:
			db = self._dbCon
		db.rollback()

	
	def _drawChart(self):
		self.setCursor(QtCore.Qt.WaitCursor)
		
		start = self.ui.comboBox_start.itemData(self.ui.comboBox_start.currentIndex()).toInt()[0]
		end = self.ui.comboBox_end.itemData(self.ui.comboBox_end.currentIndex()).toInt()[0]
		
		showConsumption = self.ui.radioButton_consumption.isChecked()
		showRevenues = self.ui.radioButton_revenues.isChecked()
		onlyNegative = self.ui.checkBox_onlyNegative.isChecked()
		personalUse = self.ui.checkBox_personalUse.isChecked()
		
		if personalUse: puWhere = ' and detail_preis = 0.0 '
		else: puWhere = ''
		
		if onlyNegative: 
			if showConsumption: 
				negHaving = ' having sum(zutate_menge*detail_absmenge) < 0 '
				negHaving2 = ' having sum(detail_absmenge) < 0 '
			if showRevenues: negHaving = ' having sum(detail_preis*detail_absmenge) < 0 '
			else: negHaving = ' having sum(detail_absmenge) < 0 '
		else:
			negHaving = ''
			negHaving2 = ''
		
		showTotal = self.ui.checkBox_showTotal.isChecked()		
		if showConsumption:
			if not showTotal:
				query = "select checkpoint_id, cast(checkpoint_info as varchar(max)), art2.artikel_bezeichnung, round(sum(zutate_menge*detail_absmenge/lager_einheit_multiplizierer), 3), count(*) "
			else: 
				query = "select 0, '01.01.1970', art2.artikel_bezeichnung, round(sum(zutate_menge*detail_absmenge/lager_einheit_multiplizierer), 3), count(*) "
			
			query += " \
					from artikel_basis as art1, artikel_basis as art2 \
					left outer join artikel_basis as ept on art2.artikel_bezeichnung = ept.artikel_bezeichnung, \
					artikel_zutaten, journal_details, journal_daten, journal_checkpoints, lager_artikel, lager_einheiten \
					where 1=1 \
					and lager_artikel_artikel = art2.artikel_id \
					and lager_artikel_einheit = lager_einheit_id \
					and detail_artikel_text = art1.artikel_bezeichnung \
					and zutate_master_artikel = art1.artikel_id \
					and zutate_istRezept = 1 \
					and zutate_artikel = art2.artikel_id \
					and detail_bonier_datum > '2008-03-31' \
					and art1.artikel_id not in (4655, 4657) \
					and ept.artikel_id not in (4655, 4657) \
					and detail_journal = daten_rechnung_id \
					and daten_checkpoint_tag = checkpoint_id \
					and checkpoint_typ = 1 \
					and daten_checkpoint_tag between %s and %s \
					 %s \
					group by checkpoint_id, cast(checkpoint_info as varchar(max)), art2.artikel_bezeichnung \
					 %s"  % (start, end, puWhere, negHaving)
					 
			query += " union all "
			
			if not showTotal: 
				query += "select checkpoint_id, cast(checkpoint_info as varchar(max)), detail_artikel_text, sum(detail_absmenge), count(*) "
			else:
				query += "select 0, '01.01.1970', detail_artikel_text, sum(detail_absmenge), count(*) "
			
			query += "from artikel_basis as a \
					left outer join artikel_zutaten \
						on zutate_master_artikel = artikel_id \
					join journal_details \
						on detail_artikel_text = artikel_bezeichnung \
					left outer join artikel_basis as ept on detail_artikel_text = ept.artikel_bezeichnung, \
					journal_daten, journal_checkpoints \
					where 1=1 \
					and zutate_istRezept is null \
					and detail_bonier_datum > '2008-03-31' \
					and a.artikel_id not in (4655, 4657) \
					and ept.artikel_id not in (4655, 4657) \
					and detail_journal = daten_rechnung_id \
					and daten_checkpoint_tag = checkpoint_id \
					and checkpoint_typ = 1 \
					and daten_checkpoint_tag between %s and %s \
					 %s \
					group by checkpoint_id, cast(checkpoint_info as varchar(max)), detail_artikel_text \
					 %s \
					order by 1" % (start, end, puWhere, negHaving2)
		else:
			if not showTotal:
				query = "select checkpoint_id, cast(checkpoint_info as nvarchar(2000)) as checkpoint_info, "
			else:
				query = "select 0, '01.01.1970' as checkpoint_info, "
			
			
			query += " detail_artikel_text, sum(detail_preis*detail_absmenge), sum(detail_absmenge) \
					from journal_checkpoints, journal_daten, journal_details \
					where 1=1 \
					and daten_checkpoint_tag = checkpoint_id \
					and daten_rechnung_id = detail_journal \
					and daten_checkpoint_tag between %s and %s \
					 %s \
					group by checkpoint_id, cast(checkpoint_info as nvarchar(2000)), detail_artikel_text \
					 %s \
					order by 1, 2, 3" % (start, end, puWhere, negHaving)
		
		print "Running query"
		print query
		results = self._runQuery(query)
		print results
		print "Query finished"
		allArticles = {}  #saves all found articles
		lastId = -1
		days = {}   #saves sold articles per day
		for r in results:
			chckId = r[0]   #checkpoint_id
			chckInfo = datetime.datetime.strptime(r[1], "%d.%m.%Y")  #checkpoint_info
			name = r[2]   # article name
			sum = r[3]
			count = r[4]
			
			if chckId != lastId:
				days[chckId] = {'info': chckInfo, 'articles': {}}
				lastId = chckId

			try:
				days[chckId]['articles'][name]['sum'] += sum
				days[chckId]['articles'][name]['count'] += count
			except KeyError:
				days[chckId]['articles'][name] = {'sum': sum, 'count': count}

			allArticles[name] = None
		
		#merge all articles into the article dict for the day
		for chckId, checkpoint in days.iteritems():
			for k in allArticles.keys():
				if k not in days[chckId]['articles']:   
					days[chckId]['articles'][k] = {'sum': 0, 'count': 0}
			
			#for name, sum in articles.iteritems():
				#print chckId, name, sum
		
		self.checkpoints = days

		if len(self.checkpoints) > 0:
			self.plot()
		else:
			ret = QtGui.QMessageBox.information(self, self.tr("Wiffzack Stats"),
                   		self.tr("No data found"),
	                   	QtGui.QMessageBox.Ok);

		self.setCursor(QtCore.Qt.ArrowCursor)
		
		
		
	def plot(self):
	
		showRevenues = self.ui.radioButton_revenues.isChecked()
		showConsumption = self.ui.radioButton_consumption.isChecked()
		chartType = self.ui.radioButton_lineChart.isChecked() and 'line' or 'bar'
		
		gv = self.ui.graphicsView_stats
		
		scene = QtGui.QGraphicsScene(gv)
		scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
		#scene.setSceneRect(-200, -200, 400, 400)
		#scene.addText("Hello, world!")
		
		
		max = 0
		for chckId, checkpoint in self.checkpoints.iteritems():
			articles = checkpoint['articles']
			for name, values in articles.iteritems():
				if showRevenues:
					if max < values['sum']: max = values['sum']
				else:
					if max < values['count']: max = values['count']
		
				
		#add legend and set colors for articles
		articles = self.checkpoints[self.checkpoints.keys()[0]]['articles']
		y = 0
		for name in sorted(articles.keys()):
			if self.activeArticles is None or name in self.activeArticles:
				if name not in self.colors:
					color = QtGui.QColor(random.randint(0,255),	random.randint(0,255),random.randint(0,255))
					self.colors[name] = color
				
				if showRevenues or showConsumption:
					text = scene.addText('%.3f' % round(articles[name]['sum'], 3)+' x '+name)
				else:
					text = scene.addText(str(articles[name]['count'])+' x '+name)
					
				text.setDefaultTextColor(self.colors[name])
				text.setPos(0, y)
				y += 20
		
		
		weekdays = self._getWeekdayList()
		
		x = LEGENDWIDTH
		oldCoords = {}
		#for chckId, checkpoint in self.checkpoints.iteritems():
		for chkId in sorted(self.checkpoints.keys()):
			checkpoint = self.checkpoints[chkId]
			if datetime.date.weekday(checkpoint['info']) in weekdays:
				articles = checkpoint['articles']
				info = checkpoint['info']
				
				#x-axis captions
				text = scene.addText(datetime.datetime.strftime(info, "%a %d.%m.%Y"))
				if chartType == 'line':
					#for line charts, show checkpoint info below every data column
					text.setPos(x-10, max+120)
					text.rotate(-90)
				else:
					#for bar charts, show the checkpoint info only once
					text.setPos(x-10, max+200)
					text.setFont(QtGui.QFont('Helvetica', 60))

					
				
				#for name, values in articles.iteritems():
				for name in sorted(articles.keys()):
					values = articles[name]
					if self.activeArticles is None or name in self.activeArticles:
					
						if chartType == 'bar':
							#x-axis captions, the article names
							text = scene.addText(name)
							text.setPos(x-10, max+200)
							text.rotate(-90)
					
						if showRevenues or showConsumption:
							v = values['sum']
						else:
							v = values['count']
						y = max - v
						color = self.colors[name]
						pen = QtGui.QPen(color)
						
						if chartType == 'bar':
							rect = Rect(QtCore.QRectF(x, max-v, 10, v))
						else:
							rect = Rect(QtCore.QRectF(x, y, 10, 10))
						rect.setPen(pen)
						rect.setBrush(color)
						rect.setAcceptHoverEvents(True)
						rect.setZValue(100)
						rect.setData(0, QtCore.QVariant(name))
						rect.setData(1, QtCore.QVariant(unicode(v)))
						rect.setData(2, QtCore.QVariant(datetime.datetime.strftime(info, "%a %d.%m.%Y")))
						
						scene.addItem(rect)
						
						if chartType == 'bar':
							x += 25
						else:
							if name in oldCoords:
								scene.addLine(oldCoords[name][0], oldCoords[name][1], x+5, y+5, pen)
							oldCoords[name] = (x+5, y+5)
				x += 100
		
		width = scene.width()+50
		
		scene.addLine(LEGENDWIDTH, max, width, max)  #x-axis
		scene.addLine(LEGENDWIDTH, 0, LEGENDWIDTH, max) #y-axis
		
		pen = QtGui.QPen(QtGui.QColor(200, 200, 200))
		for i in range(0, int(max), 100):
			scene.addLine(LEGENDWIDTH-10, max-i, width, max-i, pen)
			text = scene.addText(str(i))
			text.setPos(LEGENDWIDTH-50, max-i)
		
		gv.setScene(scene)
		gv.setCacheMode(QtGui.QGraphicsView.CacheBackground)
		gv.setRenderHint(QtGui.QPainter.Antialiasing)
		gv.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
		gv.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

		#gv.scale(0.8, 0.8)
		#gv.setMinimumSize(400, 400)


	
	def saveConf(self):
		config = ConfigParser.SafeConfigParser()
		
		#activeArticles
		if not config.has_section('activeArticles'): config.add_section("activeArticles")
		dictStream = pickle.dumps(self.activeArticles)
		config.set('activeArticles', 'articles', dictStream)
		
		if not config.has_section('weekdays'): config.add_section("weekdays")
		dictStream = pickle.dumps(self._getWeekdayList())
		config.set('weekdays', 'weekdays', dictStream)
		
		try:
			configFile = open('stats.cfg', 'w')
			config.write(configFile)
		except:
			QtGui.QMessageBox.critical(self, self.tr("Writing file failed"),
                                           'Writing the config file failed!', QtGui.QMessageBox.Ok)
		
		
		
	def loadConf(self):
		config = ConfigParser.SafeConfigParser()
		try:
			config.read('stats.cfg')
		except:
			QtGui.QMessageBox.critical(self, self.tr("Reading file failed"),
                                           'Reading the config file failed!', QtGui.QMessageBox.Ok)
			return False
		
		if not config.has_section('activeArticles'): config.add_section("activeArticles")
		try:
			self.activeArticles = pickle.loads(config.get('activeArticles', 'articles'))
		except ConfigParser.NoOptionError:
			pass
		
		if not config.has_section('weekdays'): config.add_section("weekdays")
		try:
			self._setWeekdays(pickle.loads(config.get('weekdays', 'weekdays')))
		except ConfigParser.NoOptionError:
			pass
		
		

if __name__ == "__main__":

	USER = 'wiffzack'
	PASSWORD = 'wiffzack'
	#DATABASE = 'wiffzack'
	SQLITEDB = 'WaWi.db'

	try:
	    opts, args = getopt.getopt(sys.argv[1:], "", ["host=", "database="])
	except getopt.GetoptError, err:
	    # print help information and exit:
	    print str(err) # will print something like "option -a not recognized"
	    sys.exit(2)

	for o, a in opts:
	    if o == '--host':
	        HOST = a
	    elif o == '--database':
			DATABASE = a
	    else:
	        assert False, "unhandled option"
	
	if os.name == 'nt': HOST = HOST+'/'+DATABASE
	else: HOST = HOST+':1433'
	
	if not HOST:
		print "No host specified"
		sys.exit(2)
	if not DATABASE:
		print "No database specified"
		sys.exit(2)

	
	app = QtGui.QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec_())
















