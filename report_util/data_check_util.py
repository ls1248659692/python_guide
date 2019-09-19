#!/usr/bin/python
# coding=utf8

import re
from datetime import datetime

__author__ = 'Jam'
__date__ = '2019/5/14 16:32'


def str_to_date(date_str, format="%Y%m%d"):
    return datetime.strptime(date_str, format)


def validate_decimal(value):
    if value:
        regex = re.compile(r'^([0-9]{1,}[.][0-9]*|-[0-9]{1,}[.][0-9]*|\d+|-\d+)')
        value = re.findall(regex, value)[0]
        return decimal(value)


def decimal(value):
    try:
        if value and value != "":
            return float(value)
    except:
        return 0.0
