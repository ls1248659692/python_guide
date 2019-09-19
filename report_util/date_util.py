#!/usr/bin/env python
# -*-coding:utf-8-*-

from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
import pandas as pd


def getnowtime():
    return datetime.now()


def getnowtimestr():
    return datetime.now().strftime('%Y-%m-%d')


def getdatetimestr():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def getdistime(day=1):
    return datetime.now() + timedelta(days=day)


def getyesterdaystr():
    return (datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d')


def getlastweekdaystr():
    return (datetime.now() + timedelta(days=-7)).strftime('%Y-%m-%d')


def getlastmonthstr():
    return (datetime.now() + relativedelta(months=-1)).strftime('%Y-%m-%d')


def getdisdays(maxdata, mindata):
    maxdata = checkdatestr(maxdata)
    mindata = checkdatestr(mindata)
    return (maxdata - mindata).days


def getdatestr(date):
    date = checkdatestr(date)
    return date.strftime('%Y-%m-%d')


def getyear(date):
    date = checkdatestr(date)
    return date.year


def getmonth(date):
    date = checkdatestr(date)
    return date.month


def getmonthfirstday():
    return getnowtimestr()[:8] + '01'


def getlastmonthfirstday():
    return getlastmonthstr()[:8] + '01'


def getfilestr(date):
    date = checkdatestr(date)
    return date.strftime('%Y_%m_%d')


def getdatetime(endtime):
    return datetime.strptime(endtime, '%Y-%m-%d')


def checkdatestr(date):
    if isinstance(date, str):
        date = getdatetime(date)
    return date


def change_dateformat(date, from_fmt, to_fmt):
    if isinstance(date, str):
        return datetime.strptime(date, from_fmt).strftime(to_fmt)


def datetime_offset():
    lastday = pd.to_datetime('2017-01-01', format='%Y-%m-%d')
    lastday_str = lastday.strftime('%Y-%m-%d')
    newday = lastday + pd.DateOffset(days=1)
    newdays = lastday + 1 * pd.DateOffset(days=1)
    newweek = lastday + pd.DateOffset(weeks=1)
    newweeks = lastday + 2 * pd.DateOffset(weeks=1)
    newmonth = lastday + pd.DateOffset(months=1)
    newmonths = lastday + 3 * pd.DateOffset(months=1)
    newyear = lastday + pd.DateOffset(years=1)
    newyears = lastday + 4 * pd.DateOffset(years=1)
    newdaymonthyear = lastday + pd.DateOffset(years=1, months=1, days=1)
    newdaymonthyears = lastday + 2 * pd.DateOffset(years=1, months=1, weeks=1, days=1)


if __name__ == '__main__':
    print(getdistime(2))
    print(getnowtime())
    print(getnowtimestr())
    print(getyesterdaystr())
    print(getdisdays('2018-09-01', '2018-08-01'))
    print(getdatestr('2018-01-01'))
    print(getyear('2018-01-01'))
    print(getmonth('2018-01-01'))
    print(getfilestr('2018-01-01'))
    print(getdatetime('2018-01-01'))
    print(getmonthfirstday())
    print(getlastmonthstr())
    print(getlastmonthfirstday())
    print(datetime_offset())
