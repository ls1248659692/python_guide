#!/usr/bin/python
# coding=utf8
import datetime
import threading
import time

import schedule

__author__ = 'Jam'
__date__ = '2019/3/29 14:01'


def job1():
    print "I'm working for job1"
    time.sleep(2)
    print "job1:", datetime.datetime.now()


def job2():
    print "I'm working for job2"
    time.sleep(2)
    print "job2:", datetime.datetime.now()


def job2_task():
    threading.Thread(target=job2).start()


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def run():
    schedule.every(10).seconds.do(run_threaded,job1)
    # schedule.every(10).seconds.do(job2_task)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
