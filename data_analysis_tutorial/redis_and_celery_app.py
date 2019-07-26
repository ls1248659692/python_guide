#!/usr/bin/python
# coding=utf8

__author__ = 'Jam'
__date__ = '2019/3/22 15:52'

from tasks import add

if __name__ == '__main__':
    print 'start task...'
    result = add.delay(4, 18)
    print 'end task...'
    print result
