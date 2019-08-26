#!/usr/bin/python
# coding=utf8
import pickle

import pandas as pd

__author__ = 'Jam'
__date__ = '2019/6/18 10:29'


class Graph:
    frame = pd.DataFrame()
    graph = dict()
    graph_path = 'data/person_rank.graph'

    @classmethod
    def gen_graph(cls):
        file_path = 'data/ratings.csv'
        cls.frame = pd.read_csv(file_path)
        user_ids = list(set(cls.frame['UserID']))
        item_ids = list(set(cls.frame['MovieID']))
        cls.graph = {'user_{}'.format(user_id): cls._gen_user_graph(user_id) for user_id in user_ids}
        for item_id in item_ids:
            cls.graph['item_{}'.format(item_id)] = cls._gen_item_graph(item_id)
        cls.save()

    @classmethod
    def _gen_user_graph(cls, user_id):
        print('Gen graph user: {}'.format(user_id))
        item_ids = list(set(cls.frame[cls.frame['UserID'] == user_id]['MovieID']))
        graph_dict = {'item_{}'.format(item_id): 1 for item_id in item_ids}
        return graph_dict

    @classmethod
    def _gen_item_graph(cls, item_id):
        print('Gen graph item: {}'.format(item_id))
        user_ids = list(set(cls.frame[cls.frame['MovieID'] == item_id]['UserID']))
        graph_dict = {'user_{}'.format(user_id): 1 for user_id in user_ids}
        return graph_dict

    @classmethod
    def save(cls):
        with open(cls.graph_path, 'wb') as f:
            pickle.dump(cls.graph, f)

    @classmethod
    def load(cls):
        with open(cls.graph_path, 'rb') as f:
            graph = pickle.load(f)

        return graph


class PersonalRank:

    def __init__(self):
        self.alpha = 0.6
        self.iter_count = 20
        self.graph = Graph.load()
        self.params = {k: 1 for k in self.graph.keys()}

    def train(self, user_id):
        for count in range(self.iter_count):
            print('Step {}...'.format(count))
            tmp = {k: 0 for k in self.graph.keys()}

            for node, edges in self.graph.items():
                for next_node, _ in edges.items():
                    tmp[next_node] += self.alpha * self.params[node] / len(edges)

            tmp['user_' + str(user_id)] += 1 - self.alpha
            self.params = tmp
        self.params = sorted(self.params.items(), key=lambda x: x[1], reverse=True)
        self.save(user_id)

    def predict(self, user_id, top_n=10):
        self.load(user_id)
        frame = pd.read_csv('data/ratings.csv')
        item_ids = ['item_' + str(item_id) for item_id in list(set(frame[frame['UserID'] == user_id]['MovieID']))]
        candidates = [(key, value) for key, value in self.params if key not in item_ids and 'user' not in key]
        return candidates[:top_n]

    def save(self, user_id):
        with open('data/person_rank_{}.model'.format(user_id), 'wb') as f:
            pickle.dump(self.params, f)

    def load(self, user_id):
        with open('data/person_rank_{}.model'.format(user_id), 'rb') as f:
            self.params = pickle.load(f)
