#!/usr/bin/python
# coding=utf8

import re

from quant_trade.trade_graph import read_mc_ct2df
from report_util.data_analysis_head import *

__author__ = 'Jam'
__date__ = '2018/12/26 10:31'


def read_uqr_HoldPos(ticker, beginDate, endDate):
    if re.match('\d{8}', beginDate): beginDate = beginDate[:4] + '-' + beginDate[4:6] + '-' + beginDate[6:]
    if re.match('\d{8}', endDate): endDate = endDate[:4] + '-' + endDate[4:6] + '-' + endDate[6:]

    condition = {'ticker': {"$regex": "^%s\d*" % ticker}, 'tradeDate': {"$gte": beginDate, "$lte": endDate}, 'rank': {"$lt": 20}}

    df = read_mc_ct2df('HoldPos_uqer_byD1', '_id', 'tradeDate', condition)
    if re.match('\w+\d{3,4}$', ticker):
        df_grp = df[['tradeDate', 'longVol']].fillna(0).groupby('tradeDate').count()
        if df_grp[df_grp['longVol'] > 1]: print(df_grp)
    df.index = df['tradeDate']

    beginDate = beginDate if beginDate > df.index[0] else df.index[0]
    endDate = endDate if endDate < df.index[-1] else df.index[-1]
    df = df[beginDate:endDate]
    df['partyShortName'] = df['partyShortName'].apply(lambda xx: re.sub(u'(格林大华|国投安信|五矿经易|华信万达|混沌天成|国投安信)期货', '\\1', xx, 0))
    return df


def hold_position_bypartyShortName(bname, beginDate, endDate, rank=20):
    if re.match('\d{8}', beginDate): beginDate = beginDate[:4] + '-' + beginDate[4:6] + '-' + beginDate[6:]
    if re.match('\d{8}', endDate): endDate = endDate[:4] + '-' + endDate[4:6] + '-' + endDate[6:]
    bname = ('^%s.*' % bname).decode("utf-8")

    condition = {'partyShortName': {"$regex": bname}, 'rank': {"$lt": rank}}
    df = read_mc_ct2df('HoldPos_uqer_byD1', '_id', 'tradeDate', condition)

    df.index = df['tradeDate']

    beginDate = beginDate if beginDate > df.index[0] else df.index[0]
    endDate = endDate if endDate < df.index[-1] else df.index[-1]
    df['vol'] = df[['longVol', 'shortVol']].apply(lambda xx: -1 * xx[1] if np.isnan(xx[0]) else xx[0], axis=1)
    df = df[beginDate:endDate]
    df.sort_values('ticker', inplace=True)
    print(df['tradeDate CHG vol rank ticker partyShortName'.split()])


def hold_position_byticker(ticker, beginday, endday, ranklim, show_detail=False):
    df = read_uqr_HoldPos(ticker, beginday, endday)
    df.index.name = 'dt'

    df_long = df[df['longVol'].notnull()]
    df_long = df_long[df_long['rank'] <= ranklim]
    df_long_grp = df_long[['tradeDate', 'ticker', 'longVol']].groupby(by=['tradeDate', 'ticker']).sum()

    if show_detail:
        print(df_long.sort_values(by='rank'))
        print(df_long['CHG longVol'.split()].sum())

    df_shor = df[df['shortVol'].notnull()]
    df_shor = df_shor[df_shor['rank'] <= ranklim]
    df_shor_grp = df_shor[['tradeDate', 'ticker', 'shortVol']].groupby(by=['tradeDate', 'ticker']).sum()

    if show_detail:
        print(df_shor.sort_values(by='rank'))
        print(df_shor['CHG shortVol'.split()].sum())

    df_long_grp['shorVol'] = df_shor_grp['shortVol']
    df_long_grp['diff'] = df_long_grp['longVol'] - df_long_grp['shorVol']
    df_long_grp['lim'] = ranklim
    print(df_long_grp)

def save_hold_position_bypartyShortName():
    beginday, endday = '2018-08-15', '2017-10-21'
    hold_position_bypartyShortName('中粮', beginday, beginday)


def save_hold_position_byticker():
    beginday = '2018-09-11'
    hold_position_byticker('SR', beginday, beginday, 20, True)

if __name__ == '__main__':
    # save_hold_position_bypartyShortName()
    save_hold_position_byticker()