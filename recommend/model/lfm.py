#!/usr/bin/python
# coding=utf8
import pickle
import random
from math import exp

import numpy as np
import pandas as pd

__author__ = 'Jam'
__date__ = '2019/6/18 10:29'


class Corpus:
    frame= pd.DataFrame()
    item_ids = set()
    items_dict = dict()
    items_dict_path = 'data/lfm_items.dict'

    @classmethod
    def pre_process(cls):
        file_path = 'data/ratings.csv'
        cls.frame = pd.read_csv(file_path)
        cls.user_ids = set(cls.frame['UserID'].values)
        cls.item_ids = set(cls.frame['MovieID'].values)
        cls.items_dict = {user_id: cls._get_pos_neg_item(user_id) for user_id in list(cls.user_ids)}
        cls.save()

    @classmethod
    def _get_pos_neg_item(cls, user_id):
        print('Process: {}'.format(user_id))
        pos_item_ids = set(cls.frame[cls.frame['UserID'] == user_id]['MovieID'])
        neg_item_ids = cls.item_ids ^ pos_item_ids
        neg_item_ids = list(neg_item_ids)[:len(pos_item_ids)]
        item_dict = {}
        for item in pos_item_ids: item_dict[item] = 1
        for item in neg_item_ids: item_dict[item] = 0
        return item_dict

    @classmethod
    def save(cls):
        with open(cls.items_dict_path, 'wb') as f:
            pickle.dump(cls.items_dict, f)

    @classmethod
    def load(cls):
        with open(cls.items_dict_path, 'rb') as f:
            items_dict = pickle.load(f)
        return items_dict


class LFM:

    def __init__(self):
        self.class_count = 5
        self.iter_count = 5
        self.lr = 0.02
        self.lam = 0.01
        self._init_model()

    def _init_model(self):
        file_path = 'data/ratings.csv'
        self.frame = pd.read_csv(file_path)
        self.user_ids = set(self.frame['UserID'].values)
        self.item_ids = set(self.frame['MovieID'].values)
        self.items_dict = Corpus.load()

        array_p = np.random.randn(len(self.user_ids), self.class_count)
        array_q = np.random.randn(len(self.item_ids), self.class_count)
        self.p = pd.DataFrame(array_p, columns=range(0, self.class_count), index=list(self.user_ids))
        self.q = pd.DataFrame(array_q, columns=range(0, self.class_count), index=list(self.item_ids))

    def _predict(self, user_id, item_id):
        p = np.mat(self.p.ix[user_id].values)
        q = np.mat(self.q.ix[item_id].values).T
        r = (p * q).sum()
        sig_mod = 1.0 / (1 + exp(-r))
        return sig_mod

    def _loss(self, user_id, item_id, y, step):
        e = y - self._predict(user_id, item_id)
        print('Step: {}, user_id: {}, item_id: {}, y: {}, loss: {}'.
              format(step, user_id, item_id, y, e))
        return e

    def _optimize(self, user_id, item_id, e):
        gradient_p = -e * self.q.ix[item_id].values
        l2_p = self.lam * self.p.ix[user_id].values
        delta_p = self.lr * (gradient_p + l2_p)

        gradient_q = -e * self.p.ix[user_id].values
        l2_q = self.lam * self.q.ix[item_id].values
        delta_q = self.lr * (gradient_q + l2_q)

        self.p.loc[user_id] -= delta_p
        self.q.loc[item_id] -= delta_q

    def train(self):
        for step in range(0, self.iter_count):
            for user_id, item_dict in self.items_dict.items():
                item_ids = list(item_dict.keys())
                random.shuffle(item_ids)
                for item_id in item_ids:
                    e = self._loss(user_id, item_id, item_dict[item_id], step)
                    self._optimize(user_id, item_id, e)
            self.lr *= 0.9
        self.save()

    def predict(self, user_id, top_n=10):
        self.load()
        user_item_ids = set(self.frame[self.frame['UserID'] == user_id]['MovieID'])
        other_item_ids = self.item_ids ^ user_item_ids
        interest_list = [self._predict(user_id, item_id) for item_id in other_item_ids]
        candidates = sorted(zip(list(other_item_ids), interest_list), key=lambda x: x[1], reverse=True)
        return candidates[:top_n]

    def save(self):
        with open('data/lfm.model', 'wb') as f:
            pickle.dump((self.p, self.q), f)

    def load(self):
        with open('data/lfm.model', 'rb') as f:
            self.p, self.q = pickle.load(f)
