#!/usr/bin/python
# coding=utf8
import os
import time

from model.lfm import LFM, Corpus
from setting import FILE_NOT_EXIT

__author__ = 'Jam'
__date__ = '2019/6/18 10:29'


def run():
    assert os.path.exists('data/ratings.csv'), FILE_NOT_EXIT
    print('Start..')
    start = time.time()
    if not os.path.exists('data/lfm_items.dict'):
        print('Start to Generate lfm_items.dict.')
        Corpus.pre_process()
        print('Generate lfm_items.dict ok.')
    if not os.path.exists('data/lfm.model'):
        print('Start to Generate lfm.model.')
        LFM().train()
        print('Generate lfm.model ok.')
    movies = LFM().predict(user_id=1)
    for movie in movies:
        print(movie)
    print('Cost time: %f' % (time.time() - start))


if __name__ == '__main__':
    run()
