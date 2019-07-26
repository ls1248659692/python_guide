#!/usr/bin/python
# coding=utf8
import math
import time

import pytest

__author__ = 'Jam'
__date__ = '2019/5/30 9:24'


class Circle(object):
    def __init__(self, radius, name):
        self.radius = radius
        self.__name = name

    @property
    def area(self):
        return math.pi * self.radius ** 2

    @property
    def perimeter(self):
        return 2 * math.pi * self.radius

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('%s must be str' % value)
        self.__NAME = value

    @name.deleter
    def name(self):
        raise TypeError('Can not delete')

    @classmethod
    def compute_volume(cls, height, radius):
        circle = cls(radius, 'circle')
        return height * circle.area


class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @staticmethod
    def now():
        t = time.localtime()
        return Date(t.tm_year, t.tm_mon, t.tm_mday)

    @staticmethod
    def tomorrow():
        t = time.localtime(time.time() + 86400)
        return Date(t.tm_year, t.tm_mon, t.tm_mday)


class GetDate(object):
    def __init__(self, year=0, month=0, day=0):
        self.day = day
        self.month = month
        self.year = year

    def out_date(self):
        print "year :{}, month :{}, day :{}".format(self.year, self.month, self.day)

    @classmethod
    def get_date(cls, data_as_string):
        year, month, day = map(int, data_as_string.split('-'))
        date = cls(year, month, day)
        return date

    @staticmethod
    def is_date_valid(date_as_string):
        year, month, day = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999


def unit_test():
    c = Circle(10, 'circle')
    print c.area, c.name
    print Circle.compute_volume(10, 10)

    with pytest.raises(Exception) as excinfo:
        # 此时的特性area和perimeter不能被赋值
        c.area = 3

    assert "AttributeError" in str(excinfo.typename)
    assert "can't set attribute" in str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        # 此时的特性name不能删除
        del c.name

    assert "TypeError" in str(excinfo.typename)
    assert "Can not delete" in str(excinfo.value)

    a = Date(1897, 11, 27)
    b = Date.now()
    c = Date.tomorrow()

    print(a.year, a.month, a.day)
    print(b.year, b.month, b.day)
    print(c.year, c.month, c.day)

    string_date = '2016-8-6'
    s = GetDate(*string_date.split('-'))
    s.out_date()

    r = GetDate.get_date("2016-8-6")
    r.out_date()

    is_valid = GetDate.is_date_valid('2016-8-6')
    print is_valid


if __name__ == '__main__':
    unit_test()
