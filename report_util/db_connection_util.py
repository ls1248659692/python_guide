# coding:utf-8
# !/usr/bin/env python

import traceback

import pymysql
from DBUtils.PooledDB import PooledDB
from pandas.io import sql
from sqlalchemy import create_engine

from  report_util.data_analysis_head import *

CONNECT_SUCCESS = 'Succesfully Connected to MySQL database pool. MySQL Server version is {}.'
CONNECT_ERROR = 'Error while connecting to MySQL database pool Error:{}.'

# 数据库信息
DB_CONFIG = {
    "creator": pymysql,
    "maxconnections": 5,  # maxconnections : 创建连接池的最大数量
    "mincached": 1,  # mincached 启动时开启的闲置连接数量
    "maxcached": 3,  # maxcached : 连接池中允许的闲置的最多连接数量
    "host": "****",
    "port": "****",
    "user": '****',
    "passwd": '****',
    "maxusage": 100,  # maxusage : 单个连接的最大允许复用次数,当达到最大数时,连接会自动重新连接(关闭和重新打开)
    "autocommit": False,  # 是否自动提交事物
    "blocking": False,  # blocking : 设置在连接池达到最大数量时的行为, False 等待  True报错
    "use_unicode": True,  # 字符编码
    "charset": 'utf8'  # 数据库连接编码
}

class DBPool():
    __pool = None


    def __enter__(self, db_name='ndb'):
        self.conn = DBPool.get_conn(db_name)
        self.cursor = self.conn.cursor()
        return self

    @staticmethod
    def get_conn(db_name):
        if DBPool.__pool is None:
            try:
                db_pool = PooledDB(db=db_name, **DB_CONFIG)
                version = db_pool.version

                print (CONNECT_SUCCESS.format(version))
                return db_pool.connection()

            except Exception as error:
                traceback.print_exc()
                print (CONNECT_ERROR.format(error))
                return CONNECT_ERROR.format(error)

        return DBPool.__pool.connection()

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()


def read_ndb_sql(sql):
    with DBPool() as db:
        try:
            db.conn.ping()
            conn = db.conn
        except Exception as error:
            traceback.print_exc()
            return CONNECT_ERROR.format(error)

        return pd.read_sql(sql, conn)


def ndb_sql_execute(sql_str, args):
    conn = create_engine(
        'mysql://{0}:{1}@{2}:{3}/ndb?charset=utf8'.format(
            DB_CONFIG['user'],DB_CONFIG['passwd'],DB_CONFIG['host'],DB_CONFIG['port']
        )
    ).connect()

    try:
        sql.execute(sql_str, conn, params=[args])
    except  Exception as error:
        conn.rollback()
        traceback.print_exc()
        conn.close()
        return CONNECT_ERROR.format(error)
    finally:
        conn.close()
        return True


def query(sql, args=None):
    with DBPool() as db:
        try:
            db.conn.ping()
        except Exception as error:
            traceback.print_exc()
            return CONNECT_ERROR.format(error)

        cur = db.cursor
        cur.execute(sql, args)
        return cur.fetchall()


def execute(sql, args=None):
    with DBPool() as db:
        try:
            cur = db.cursor
            result = cur.execute(sql, args)
            db.conn.commit()
            return result
        except Exception as error:
            db.conn.rollback()
            traceback.print_exc()
            return CONNECT_ERROR.format(error)


def executmany(sql, args=None):
    with DBPool() as db:
        try:
            cur = db.cursor
            result = cur.executemany(sql, args)
            db.conn.commit()
            return result
        except Exception as error:
            db.conn.rollback()
            traceback.print_exc()
            return CONNECT_ERROR.format(error)


def test_read_sql():
    sql = '''SELECT * FROM ndb_user LIMIT 10'''
    results = query(sql)
    print (results)

    df = read_ndb_sql(sql)
    print (df)

    ndb_sql_execute('INSERT INTO test.cox_cc VALUES(%s,%s)', (1, 200.00))


if __name__ == '__main__':
    test_read_sql()
