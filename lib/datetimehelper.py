# -*- coding: utf-8 -*-

import calendar
import datetime

maxDate = datetime.datetime(2099, 12, 31, 23, 59, 59)

def getMonthBeginEnd(date=None):
	if date is None:
		date = datetime.datetime.now()
		
	year = date.year
	month = date.month
	lastDay = calendar.monthrange(year, month)[1]
	monthBegin = datetime.date(year, month, 1)
	monthEnd = datetime.date(year, month, lastDay)
	
	return (monthBegin, monthEnd)

