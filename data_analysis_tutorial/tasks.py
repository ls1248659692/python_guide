#!/usr/bin/python
# coding=utf8
import time

from celery import Celery

__author__ = 'Jam'
__date__ = '2019/3/22 15:50'

broker = 'redis://192.168.5.141:6379/1'
backend = 'redis://192.168.5.141:6379/2'
app = Celery('my_task', broker=broker, backend=backend)


@app.task
def add(x, y):
    print 'enter call func....'
    time.sleep(4)
    return x + y
