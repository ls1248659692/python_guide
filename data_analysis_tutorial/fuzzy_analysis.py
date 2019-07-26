#!/usr/bin/python
# coding=utf8
import difflib

from fuzzywuzzy import fuzz

__author__ = 'Jam'
__date__ = '2019/4/23 16:54'

s1 = u"你们公司在哪里"
s2 = u"你家的公司地址在哪里"

print(fuzz.ratio(s1, s2))
print(fuzz.partial_ratio(s1, s2))

a = u'研报标题：价格怎么样'
b = u'价格怎么卖'
print(difflib.SequenceMatcher(None, a, b).ratio())
