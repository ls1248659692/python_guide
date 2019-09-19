# coding:utf-8
# !/usr/bin/env python
import json
import traceback

import pandas as pd

from pymongo import MongoClient

from .constant import MONGODB_CONFIG
from report_util.date_util import getmonthfirstday, getlastmonthfirstday

conn = MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])


def save_df_mongo(df, collect):
    collect = conn.Oanda_info[collect]
    records = json.loads(df.T.to_json()).values()
    collect.insert_many(records)


def save_log_bymongo(df, collect):
    collect = conn.Apilog[collect]
    records = json.loads(df.T.to_json()).values()
    collect.insert_many(records)


def load_mongo_data_bydf(collect, condition={}, db="Oanda_info"):
    if db != "Oanda_info":
        mcdb = conn[db]
        collect = mcdb[collect]
    else:
        collect = conn.Oanda_info[collect]
    df = pd.DataFrame(list(collect.find(condition)))
    if not df.empty:
        del df['_id']
        # df.drop(columns=['_id'], inplace=True)
    return df


def rename_mongo_collection_columns():
    collect = 'HangQing_idxcons_csindex'
    db = conn['Oanda_info'][collect]
    db.update_many({}, {'$rename': {'Date': 'date'}})
    db.update_many({}, {'$rename': {'Index_Code': 'indexCode'}})
    db.update_many({}, {'$rename': {'Index_Chinese_Name(Full)': 'indexChineseName(Full)'}})
    db.update_many({}, {'$rename': {'Index_Chinese_Name': 'indexChineseName'}})
    db.update_many({}, {'$rename': {'Index_English_Name(Full)': 'indexEnglishName(Full)'}})
    db.update_many({}, {'$rename': {'Index_English_Name': 'indexEnglishName'}})
    db.update_many({}, {'$rename': {'Open': 'open'}})
    db.update_many({}, {'$rename': {'High': 'high'}})
    db.update_many({}, {'$rename': {'Low': 'low'}})
    db.update_many({}, {'$rename': {'Close': 'close'}})
    db.update_many({}, {'$rename': {'Change': 'change'}})
    db.update_many({}, {'$rename': {'Change_rate(%)': 'changeRate(%)'}})
    db.update_many({}, {'$rename': {'Turnover': 'turnover'}})
    db.update_many({}, {'$rename': {'Volume': 'volume'}})
    db.update_many({}, {'$rename': {'Index_Name': 'indexName'}})
    db.update_many({}, {'$rename': {'Index_Name(Eng)': 'indexName(Eng)'}})
    db.update_many({}, {'$rename': {'Constituent_Code': 'constituentCode'}})
    db.update_many({}, {'$rename': {'Constituent_Name': 'constituentName'}})
    db.update_many({}, {'$rename': {'Constituent_Name(Eng)': 'constituentName(Eng)'}})
    db.update_many({}, {'$rename': {'Exchange': 'exchange'}})


def clean_mongodb_collect_duplicate_data(collesct_name, db="Oanda_info"):
    if db == "Oanda_info":
        collect = conn.Oanda_info[collesct_name]

        ticker_td = set()
        this_month_firstday = getmonthfirstday()

        last_month_firstday = int(getlastmonthfirstday().replace('-', ''))

        condiction = {
            "date": {"$gte": last_month_firstday}} if collesct_name == 'Hibor_news' else {
            "tradeDate": {"$gte": this_month_firstday}}

        for duplicate_data in collect.find(condiction):
            if collesct_name == 'HoldPos_uqer_byD1':
                if 'longVol' in duplicate_data.keys():
                    key_list = ['partyShortName', 'ticker', 'tradeDate', 'CHG', 'longVol']
                else:
                    key_list = ['partyShortName', 'ticker', 'tradeDate', 'CHG', 'shortVol']
            elif collesct_name == 'Hibor_news':
                key_list = ['url']
            else:
                key_list = ['ticker', 'tradeDate']

            str_ticker_key = ' '.join(map(str, [duplicate_data[key] for key in key_list]))

            if str_ticker_key not in ticker_td:
                ticker_td.add(str_ticker_key)
            else:
                id = duplicate_data['_id']
                collect.remove({'_id': id})


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


class MongoConn(Singleton):
    def __init__(self):
        try:
            self.conn = MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
            self.username = MONGODB_CONFIG['username']
            self.password = MONGODB_CONFIG['password']

            if self.username and self.password:
                uri = ('mongodb://' + MONGODB_CONFIG['username'] + ':' +
                       MONGODB_CONFIG['password'] + '@' +
                       MONGODB_CONFIG['host'] + ':' +
                       MONGODB_CONFIG['port'])
                self.conn = MongoClient(uri)

        except Exception:
            print(traceback.format_exc())
            print('Connect Statics Database Fail.')

    def connect_db(self, db_name):
        db = self.conn[db_name]
        return db

    def save(self, db_name, table, value):
        try:
            db = self.conn[db_name]
            db[table].save(value)
        except Exception:
            print(traceback.format_exc())

    def insert(self, db_name, table, value):
        try:
            db = self.conn[db_name]
            db[table].insert(value, continue_on_error=True)
        except Exception:
            print(traceback.format_exc())

    def update(self, db_name, table, conditions, value, s_upsert=False, s_multi=False):
        try:
            db = self.conn[db_name]
            db[table].update(conditions, value, upsert=s_upsert, multi=s_multi)
        except Exception:
            print(traceback.format_exc())

    def upsert_many(self, db_name, table, datas):
        try:
            db = self.conn[db_name]
            bulk = db[table].initialize_ordered_bulk_op()
            for data in datas:
                _id = data['_id']
                bulk.find({'_id': _id}).upsert().update({'$set': data})
            bulk.execute()
        except Exception:
            print(traceback.format_exc())

    def upsert_one(self, db_name, table, data):
        try:
            query = {'_id': data.get('_id', '')}
            db = self.conn[db_name]
            if not db[table].find_one(query):
                db[table].insert(data)
            else:
                data.pop('_id')
                db[table].update(query, {'$set': data})
        except Exception:
            print(traceback.format_exc())

    def find_one(self, db_name, table, value):
        try:
            db = self.conn[db_name]
            return db[table].find_one(value)
        except Exception:
            print(traceback.format_exc())

    def find(self, db_name, table, value):
        try:
            db = self.conn[db_name]
            return db[table].find(value)
        except Exception:
            print(traceback.format_exc())

    def select_colum(self, db_name, table, value, colum):
        try:
            db = self.conn[db_name]
            return db[table].find(value, colum)
        except Exception:
            print(traceback.format_exc())


if __name__ == '__main__':
    # rename_mongo_collection_columns()
    # clean_mongodb_collect_duplicate_data('HangQing_investing_byD1')
    pass
