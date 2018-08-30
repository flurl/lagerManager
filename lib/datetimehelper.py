# -*- coding: utf-8 -*-

import calendar
import datetime
from dateutil.relativedelta import relativedelta


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


def now():
    return datetime.datetime.now()
    

def today():
    return datetime.date.today()


def addMonths(date, count):
    delta = relativedelta(months=count)
    return date+delta
    

def addWeeks(date, count):
    delta = relativedelta(weeks=count)
    return date+delta
    
    
def daysBetween(d1, d2):
    return abs((d2 - d1).days)
