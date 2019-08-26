#!/usr/bin/python
# coding=utf8
import os
import time

from model.cf import UserCf
from setting import FILE_NOT_EXIT

__author__ = 'Jam'
__date__ = '2019/6/18 11:27'


def run():
    assert os.path.exists('data/ratings.csv'), FILE_NOT_EXIT
    print('Start..')
    start = time.time()
    movies = UserCf().calculate()
    for movie in movies:
        print(movie)
    print('Cost time: %f' % (time.time() - start))


if __name__ == '__main__':
    run()
