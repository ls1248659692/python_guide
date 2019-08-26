#!/usr/bin/python
# coding=utf8
import math

import pandas as pd

__author__ = 'Jam'
__date__ = '2019/6/18 10:29'


class UserCf:

    def __init__(self):
        self.file_path = 'data/ratings.csv'
        self._init_frame()

    def _init_frame(self):
        self.frame = pd.read_csv(self.file_path)

    @staticmethod
    def _cosine_sim(target_movies, movies):
        union_len = len(set(target_movies) & set(movies))
        if union_len == 0: return 0.0
        product = len(target_movies) * len(movies)
        cosine = union_len / math.sqrt(product)
        return cosine

    def _get_top_n_users(self, target_user_id, top_n):
        target_movies = self.frame[self.frame['UserID'] == target_user_id]['MovieID']
        other_users_id = [i for i in set(self.frame['UserID']) if i != target_user_id]
        other_movies = [self.frame[self.frame['UserID'] == i]['MovieID'] for i in other_users_id]

        sim_list = [self._cosine_sim(target_movies, movies) for movies in other_movies]
        sim_list = sorted(zip(other_users_id, sim_list), key=lambda x: x[1], reverse=True)
        return sim_list[:top_n]

    def _get_candidates_items(self, target_user_id):
        target_user_movies = set(self.frame[self.frame['UserID'] == target_user_id]['MovieID'])
        other_user_movies = set(self.frame[self.frame['UserID'] != target_user_id]['MovieID'])
        candidates_movies = list(target_user_movies ^ other_user_movies)
        return candidates_movies

    def _get_top_n_items(self, top_n_users, candidates_movies, top_n):
        top_n_user_data = [self.frame[self.frame['UserID'] == k] for k, _ in top_n_users]
        interest_list = []
        for movie_id in candidates_movies:
            tmp = []
            for user_data in top_n_user_data:
                if movie_id in user_data['MovieID'].values:
                    tmp.append(user_data[user_data['MovieID'] == movie_id]['Rating'].values[0] / 5)
                else:
                    tmp.append(0)
            interest = sum([top_n_users[i][1] * tmp[i] for i in range(len(top_n_users))])
            interest_list.append((movie_id, interest))
        interest_list = sorted(interest_list, key=lambda x: x[1], reverse=True)
        return interest_list[:top_n]

    def calculate(self, target_user_id=1, top_n=10):
        # most similar top n users
        top_n_users = self._get_top_n_users(target_user_id, top_n)

        # candidates movies for recommendation
        candidates_movies = self._get_candidates_items(target_user_id)

        # most interest top n movies
        top_n_movies = self._get_top_n_items(top_n_users, candidates_movies, top_n)
        return top_n_movies
