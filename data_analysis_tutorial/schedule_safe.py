#!/usr/bin/python
# coding=utf8
import Queue
import time
import threading

import schedule

__author__ = 'Jam'
__date__ = '2019/3/29 14:23'

jobqueue = Queue.Queue()


def job():
    print "I'm working"


def worker_main():
    while True:
        job_func = jobqueue.get()
        job_func()


def run():
    schedule.every(10).seconds.do(jobqueue.put, job)
    schedule.every(10).seconds.do(jobqueue.put, job)
    schedule.every(10).seconds.do(jobqueue.put, job)
    schedule.every(10).seconds.do(jobqueue.put, job)
    schedule.every(10).seconds.do(jobqueue.put, job)

    worker_thread = threading.Thread(target=worker_main)
    worker_thread.start()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
