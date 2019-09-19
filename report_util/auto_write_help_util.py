#!/usr/bin/python
# coding=utf8
import os
import sys

import tornado

__author__ = 'Jam'
__date__ = '2019/1/16 11:58'

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def write_help_file():
    out = sys.stdout
    sys.stdout = open(PROJECT_ROOT + '\static\help_file\{}.txt'.format(tornado.__name__), 'w')
    help(tornado)
    sys.stdout.close()
    sys.stdout = out


if __name__ == "__main__":
    write_help_file()
