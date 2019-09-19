#!/usr/bin/python
# coding=utf8
import sys
import os

base_dir = os.path.dirname(os.path.abspath('.'))
sys.path.append(base_dir)
# print base_dir, sys.path

import argparse

__author__ = 'Jam'
__date__ = '2019/2/20 17:27'


def setup_argparse():
    parser = argparse.ArgumentParser(description=u'测试下python中的argparse')
    parser.add_argument('-s', action=u'store', dest='start_date', required=True, help=u'开始采集日期')
    parser.add_argument('-e', action=u'store', dest='end_date', required=True, help=u'结束采集日期')

    # group = parser.add_mutually_exclusive_group()
    # group.add_argument("-v", "--verbose", action="store_true")
    # group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("-x", type=int, help="the base")
    parser.add_argument("-y", type=int, help="the exponent")
    args = parser.parse_args()

    ## python2 argparse_util.py -s '2019-01-01' -e '2019-02-01' -q 1 2
    ## python2 argparse_util.py -s '2019-01-01' -e '2019-02-01' -v 1 2

    print (args)
    print( args.start_date, args.end_date)
    print( args.x, args.y)

if __name__ == '__main__':
    setup_argparse()
