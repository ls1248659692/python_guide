#!/usr/bin/python
# coding=utf8
import os
import time

from model.personal_rank import Graph, PersonalRank
from setting import FILE_NOT_EXIT

__author__ = 'Jam'
__date__ = '2019/6/18 10:29'


def run():
    assert os.path.exists('data/ratings.csv'), FILE_NOT_EXIT
    print('Start..')
    start = time.time()
    if not os.path.exists('data/person_rank.graph'):
        Graph.gen_graph()
    if not os.path.exists('data/person_rank_1.model'):
        PersonalRank().train(user_id=1)
    movies = PersonalRank().predict(user_id=1)
    for movie in movies:
        print(movie)
    print('Cost time: %f' % (time.time() - start))


if __name__ == '__main__':
    run()
