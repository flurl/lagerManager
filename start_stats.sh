#!/bin/bash

echo "Connect to"
echo "1) Postgarage"
echo "2) Postgarage Backup"
echo "3) Cafe"
echo "4) Cafe Backup"
read -p "Make your choice (1=default): " CHOICE

if [ X$CHOICE == "X1" ]; then
	HOST=192.168.100.140
	DB=wiffzack
elif [ X$CHOICE == "X2" ]; then
        HOST=192.168.2.100
        DB=wiffzack_backup
elif [ X$CHOICE == "X3" ]; then
        HOST=192.168.3.100
        DB=wiffzack
elif [ X$CHOICE == "X4" ]; then
        HOST=192.168.3.100
        DB=wiffzack_backup
else
        HOST=192.168.100.140
        DB=wiffzack
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo $HOST $DB

cd $DIR
python stats.py --host=$HOST --database=$DB
