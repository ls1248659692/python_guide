#!/usr/bin/python
# coding=utf8
import pandas as pd

__author__ = 'Jam'
__date__ = '2019/6/18 11:27'


class Preprocesss:

    def __init__(self):
        self.origin_path = 'data/{}'

    def process(self):
        print('Start data pre-processing.')
        self._process_user_data()
        self._process_movies_date()
        self._process_rating_data()
        print('End of data pre-processing.')

    def _process_user_data(self, file='users.dat'):
        data = pd.read_table(self.origin_path.format(file), sep='::', engine='python',
                             names=['userID', 'Gender', 'Age', 'Occupation', 'Zip-code'])
        data.to_csv(self.origin_path.format('users.csv'), index=False)

    def _process_rating_data(self, file='ratings.dat'):
        data = pd.read_table(self.origin_path.format(file), sep='::', engine='python',
                             names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
        data.to_csv(self.origin_path.format('ratings.csv'), index=False)

    def _process_movies_date(self, file='movies.dat'):
        data = pd.read_table(self.origin_path.format(file), sep='::', engine='python',
                             names=['MovieID', 'Title', 'Genres'])
        data.to_csv(self.origin_path.format('movies.csv'), index=False)


def run():
    Preprocesss().process()


if __name__ == '__main__':
    Preprocesss().process()
