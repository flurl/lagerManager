Requirements:
Python
PyQT4
pymssql
ConfigObj (easy_install configobj)
FreeTDS (enable utf-8 in freetds.conf - "client charset = UTF-8") 
dateutil

sudo apt-get install python2.7 python-qt4 python-qt4-sql libqt4-sql-mysql python-pymssql freetds-bin python-setuptools python-dateutil
sudo easy_install configobj

Ubuntu >= 12.04 has incompatibilities between pymssql and freetds 0.9x (see https://bugs.launchpad.net/ubuntu/+source/pymssql/+bug/918896).
To resolve do the following:
	apt-get remove python-pymssql
	apt-get install python-dev freetds-dev
	easy_install pymssql
