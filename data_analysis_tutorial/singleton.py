#!/usr/bin/python
# coding=utf8

__author__ = 'Jam'
__date__ = '2019/1/11 15:25'


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._inst


class A(Singleton):
    def __init__(self, s):
        self.s = s


if __name__ == '__main__':
    ## 单例设计模式用于有减少重复创建实例需求的场景，例如windows的回收站页面，短信发送对象等业务场景,减少服务器的压力
    a = A('apple')
    print id(a), a.s
    b = A('asasasas')
    print id(b), b.s

