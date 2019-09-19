#!/usr/bin/python
# coding=utf8

__author__ = 'Jam'
__date__ = '2019/5/29 10:25'


class EmptyError(Exception):
    """自定义空异常类"""
    pass


class RequestError(Exception):
    """自定义访问请求类"""
    pass


def test_rexception1():
    try:
        raise EmptyError('empty container')
    except:
        pass


def test_rexception2():
    try:
        raise RequestError('empty container')
    except:
        pass


if __name__ == '__main__':
    test_rexception1()
    test_rexception2()
