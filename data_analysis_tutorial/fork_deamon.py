#!/usr/bin/python
# coding=utf8
import os
import time

__author__ = 'Jam'
__date__ = '2019/6/26 10:40'


def test_deamon():
    # windows内核中没有os.fork()函数，需要在其他环境上测试
    number = 7

    print 'Process (%s) start...' % os.getpid()
    try:
        pid = os.fork()
        print pid

        if pid == 0:
            print 'I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid())
            number = number - 1
            time.sleep(5)
            print number
        else:
            print 'I (%s) just created a child process (%s).' % (os.getpid(), pid)
            print number
    except OSError, e:
        pass


if __name__ == '__main__':
    test_deamon()
