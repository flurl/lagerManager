# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from ui.connectDlg_gui import Ui_ConnectDialog

import config
import DBConnection


class ConnectDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.ui = Ui_ConnectDialog()
        self.ui.setupUi(self)

        self.connect(self.ui.pushButton_connect, QtCore.SIGNAL('clicked()'),
                    self.connectToDb)
        self.connect(self.ui.comboBox_connection,
                     QtCore.SIGNAL('currentIndexChanged (const QString&)'),
                     self.loadStoredConnection)

        try:
            c = config.config['app_db_connections']
            for conn in c.keys():
                self.ui.comboBox_connection.addItem(conn)
        except KeyError:
            pass

        self.loadStoredConnection(
                                 unicode(self.ui.comboBox_connection.
                                        currentText()))

    def connectToDb(self):
        host = unicode(self.ui.lineEdit_host.text())
        db = unicode(self.ui.lineEdit_db.text())
        user = unicode(self.ui.lineEdit_user.text())
        pw = unicode(self.ui.lineEdit_pw.text())
        connName = unicode(self.ui.comboBox_connection.currentText())

        if DBConnection.connect(host, user, pw, db, connName):
            connParams = {'host': host, 'db': db, 'user': user}
            try:
                c = config.config['app_db_connections']
            except KeyError:
                c = config.config['app_db_connections'] = {}

            if connName != '':
                c[connName] = connParams

            config.config.write()
            self.accept()
        else:
            QtGui.QMessageBox.critical(self, 'Verbindung fehlgeschlagen',
                                      'Verbindung fehlgeschlagen',
                                      QtGui.QMessageBox.Ok)

    def loadStoredConnection(self, name):
        name = unicode(name)
        try:
            c = config.config['app_db_connections'][name]
            self.ui.lineEdit_host.setText(c['host'])
            self.ui.lineEdit_db.setText(c['db'])
            self.ui.lineEdit_user.setText(c['user'])
        except KeyError:
            pass
