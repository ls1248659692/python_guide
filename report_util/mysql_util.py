#!/usr/bin/python
# coding=utf8
import traceback

import pymysql


from sqlalchemy import create_engine

from .data_analysis_head import *
from report_util.constant import MYSQL_CONFIG_95, MYSQL_CONFIG_87, MYSQL_CONFIG_73, MYSQL_CONFIG_254

__author__ = 'Jam'
__date__ = '2019/1/18 10:14'


def execute(db_num, sql):
    if db_num == '95':
        config = MYSQL_CONFIG_95
    elif db_num == '87':
        config = MYSQL_CONFIG_87
    elif db_num == '73':
        config = MYSQL_CONFIG_73
    elif db_num == '254':
        config = MYSQL_CONFIG_254

    conn = pymysql.connect(**config)

    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except BaseException:
        conn.rollback()
        traceback.print_exc()
    finally:
        conn.close()


def executemany(db_num, sql, param):
    if db_num == '95':
        config = MYSQL_CONFIG_95
    elif db_num == '87':
        config = MYSQL_CONFIG_87
    elif db_num == '73':
        config = MYSQL_CONFIG_73
    elif db_num == '254':
        config = MYSQL_CONFIG_254

    conn = pymysql.connect(**config)

    try:
        cur = conn.cursor()
        cur.executemany(sql, param)
        conn.commit()
    except BaseException:
        conn.rollback()
        traceback.print_exc()
    finally:
        conn.close()


def read_sql(db_num, sql, cols=None):
    if db_num == '95':
        config = MYSQL_CONFIG_95
    elif db_num == '87':
        config = MYSQL_CONFIG_87
    elif db_num == '73':
        config = MYSQL_CONFIG_73
    elif db_num == '254':
        config = MYSQL_CONFIG_254

    conn = pymysql.connect(**config)

    df = pd.read_sql(sql, conn)
    if cols is not None:
        df = df[cols]

    return df


def save_data(db_num, df, table):
    if len(df) == 1:
        sql = '''
                INSERT INTO {table}
                    ({cols})
                VALUES
                    ({vals})
        '''.format(
            table=table,
            cols=','.join(df.columns),
            vals=','.join(["\"" + str(val) + "\"" for val in df.values[0]])
        )

        execute(db_num, sql)
    elif len(df) > 1:
        param = df.values.tolist()

        sql = '''
                INSERT INTO {table}
                    ({cols})
                VALUES
                    ({vals})
        '''.format(
            table=table,
            cols=','.join(df.columns),
            vals=','.join('%s' for _ in df.columns)
        )

        executemany(db_num, sql, param)
    else:
        print('dataframe is empty, please check reason.')


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._inst


class PandasMysql(Singleton):
    db_url = 'mysql+mysqldb://{user}:{passwd}@{host}:{port}/{db}?charset={charset}'

    def df_to_new_table(self, db_config, db_table, data_frame, data_type=None):
        engine = create_engine(self.db_url.format(**db_config))
        # forbid to use  if_exists='fail', table should not to be modify
        data_frame.to_sql(name=db_table, con=engine, if_exists='fail', index=False, chunksize=5000, dtype=data_type)

    def df_to_exist_table(self, db_config, db_table, data_frame, data_type=None):
        engine = create_engine(self.db_url.format(**db_config))
        data_frame.to_sql(name=db_table, con=engine, if_exists='append', index=False, chunksize=5000, dtype=data_type)

    def export_sql_to_df(self, db_config, sql):
        conn = pymysql.connect(**db_config)
        data_frame = pd.read_sql(sql, conn)
        return data_frame


DB_CONN = PandasMysql()
