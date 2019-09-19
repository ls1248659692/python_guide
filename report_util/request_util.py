#!/usr/bin/python
# coding=utf8
import time
import timeit

import requests
import grequests

__author__ = 'Jam'
__date__ = '2018/12/25 16:34'


def greq():
    urls = [
        'http://www.heroku.com',
        'http://python-tablib.org',
        'http://httpbin.org',
        'http://python-requests.org',
        'http://kennethreitz.com'
    ]
    start = time.time()
    rs = (grequests.get(u) for u in urls)
    responses = grequests.map(rs, size=5)
    print  time.time() - start


def req():
    urls = [
        'http://www.heroku.com',
        'http://python-tablib.org',
        'http://httpbin.org',
        'http://python-requests.org',
        'http://kennethreitz.com'
    ]

    start = time.time()

    for i in urls:
        response = requests.get(i)
        print(i)

    print  time.time() - start

if __name__ == '__main__':
    print("user-grequests", timeit.timeit(stmt=greq, number=1))
    print("user-requests", timeit.timeit(stmt=req, number=1))
