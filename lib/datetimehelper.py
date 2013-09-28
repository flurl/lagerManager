# -*- coding: utf-8 -*-

import calendar
import datetime


def getMonthBeginEnd(self, date=None):
	if date is None:
		date = datetime.datetime.now()
		
	year = date.year
	month = date.month
	lastDay = calendar.monthrange(year, month)[1]
	monthBegin = datetime.date(year, month, 1)
	monthEnd = datetime.date(year, month, lastDay)
	
	return (monthBegin, monthEnd)