#!/usr/bin/python
# coding=utf8

import redis

__author__ = 'Jam'
__date__ = '2019/3/22 16:27'

r = redis.Redis(host='192.168.5.141', port=6379, db=0)
r.set('name', 'liangshuang')
r.set('test_time', 'my_first_time')

print  r.get('name')
print  r.get('test_time')
