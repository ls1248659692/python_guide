#!/usr/bin/python
# coding=utf8
import os
import re

from pymongo import MongoClient

from pyecharts import Line, Page, Grid

from quant_trade.constant import Path
from report_util.data_analysis_head import *

__author__ = 'Jam'
__date__ = '2018/12/6 15:35'

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
FILE_DIR = os.path.join(PROJECT_ROOT, Path.STATIC_HTML_PATH)
PIC_FILE_PATH = os.path.join(PROJECT_ROOT, Path.STATIC_PIC_PATH)


def read_mc_ct2df(collect, id_col, sort_col, condition={}, db="Oanda_info"):
    mclient = MongoClient('192.168.5.220:27017')

    if db != "Oanda_info":
        mcdb = mclient[db]
        collect = mcdb[collect]
    else:
        collect = mclient.Oanda_info[collect]

    df0 = pd.DataFrame(list(collect.find(condition)))
    df0 = df0.set_index(id_col)
    df0 = df0.sort_values(sort_col)
    return df0


def read_uqr_HangQing(ticker, beginDate, endDate, ismain=0):
    if re.match('\d{8}', beginDate): beginDate = beginDate[:4] + '-' + beginDate[4:6] + '-' + beginDate[6:]
    if re.match('\d{8}', endDate): endDate = endDate[:4] + '-' + endDate[4:6] + '-' + endDate[6:]

    condition = {'ticker': {"$regex": "^%s\d*$" % ticker}}
    df = read_mc_ct2df('HangQing_qh_uqer_byD1', '_id', 'tradeDate', condition)

    df.index = df['tradeDate']
    df.index.name = 'dt'
    df = df.sort_index()

    df = df[beginDate:endDate]
    if ismain == 1: df = df[df['mainCon'] == 1]
    return df


def contr_end_val(nar):
    res_li = []
    nar = nar[::-1]
    dic_contr = {}
    for dt, cl, cl_lag, contr, contr_lag in nar.values:
        if contr_lag not in dic_contr:
            end_cl, end_cl_lag = np.NAN, np.NAN
        if contr_lag not in dic_contr and re.sub('-', '', dt[2:7]) < contr_lag[-4:]:
            end_cl, end_cl_lag = cl, cl_lag
            dic_contr[contr_lag] = 1

        res_li.append((end_cl, end_cl_lag))
    res_li = res_li[::-1]
    return res_li


def tiesheng_shui(contract, aft_emptycontr):
    startday, endday = "20110101", '2019-12-31'
    if contract == "ZC":
        df0 = read_uqr_HangQing("TC", startday, "20160101", ismain=1)['closePrice tradeDate ticker'.split()]
        df1 = read_uqr_HangQing(contract, startday, "20190101", ismain=1)['closePrice tradeDate ticker'.split()]
        df0 = pd.concat([df0, df1])
    else:
        df0 = read_uqr_HangQing(contract, startday, "20200101", ismain=1)['closePrice tradeDate ticker'.split()]
    df0 = df0['ticker tradeDate closePrice '.split()].drop_duplicates(subset='tradeDate', keep='first').sort_values(by='tradeDate').set_index('tradeDate')

    df = df0.copy()
    df['tradeDate'] = df.index.map(lambda xx: str(xx))
    if contract == "SF":
        df = df[~(df['tradeDate'].str.match('2016-0[89]') & df['ticker'].str.match('SF7'))]
        df = df[~(df['tradeDate'].str.match('2017-0[23]') & df['ticker'].str.match('SF8'))]
        df = df[~(df['tradeDate'].str.match('\d\d\d\d-12') & df['ticker'].str.match('.*1$'))]
        # df = df[~(df['tradeDate'].str.match('\d\d\d\d-08') & df['ticker'].str.match('.*9$'))]
        df = df[df['ticker'].str.match('.*[159]$')]
        df = df.dropna()
    if contract == "m":
        df = df[~(df['tradeDate'].str.match('2014-0[78]') & df['ticker'].str.match('m1505'))]
    if contract == contract.upper(): aft_emptycontr = aft_emptycontr[1:]
    df['tick_lag'] = list(df['ticker'].values[1:]) + [contract + aft_emptycontr] * 1
    df['tick_chg'] = (df['tick_lag'] != df['ticker'])

    shiftk = 1
    if shiftk > 0:
        df['tick_kk'] = [None] * shiftk + list(df['ticker'].values[:-shiftk])
        df['tick_chg_kk'] = [False] * shiftk + list(df['tick_chg'].values[:-shiftk])
        df.loc[df.index[-1], 'tick_chg_kk'] = True
    else:
        df['tick_kk'] = df['ticker']
        df['tick_chg_kk'] = df['tick_chg']
    # print df.tail(30)

    df_tklag = df[df['tick_chg_kk']]
    df_tklag.loc[:, 'dt'] = df_tklag.index
    df_tklag.loc[:, 'dt_lag'] = [np.NAN] * 1 + list(df_tklag.index[:-1])
    df_tklag.loc[:, 'dt_lag'] = df_tklag['dt_lag'].fillna(endday)

    df_li = [[], []]
    for tick, tick_lag, dt_lag, dt in df_tklag['tick_kk tick_lag dt_lag dt'.split()].values[1:]:
        dt = re.sub('-', '', dt, 0)
        dt_lag = re.sub('-', '', dt_lag, 0)
        beginDate, endDate = (dt_lag, dt)
        # print(tick, tick_lag, beginDate, endDate)
        df_tk = read_uqr_HangQing(tick, beginDate, endDate, ismain=0)['closePrice ticker tradeDate'.split()]
        df_tklag = read_uqr_HangQing(tick_lag, beginDate, endDate, ismain=0)['closePrice ticker tradeDate'.split()]
        # print df_tmp.head(10)
        df_li[0].append(df_tk)
        df_li[1].append(df_tklag)
    df_main = pd.concat(df_li[0])
    df_lag = pd.concat(df_li[1])

    df_main = df_main['ticker tradeDate closePrice'.split()].drop_duplicates(subset='tradeDate', keep='first').set_index('tradeDate')
    df_lag = df_lag['ticker tradeDate closePrice'.split()].drop_duplicates(subset='tradeDate', keep='first').set_index('tradeDate')
    df_lag['tick_lag'] = df_lag['ticker']
    df_lag['lag_pr'] = df_lag['closePrice']
    del df_lag['closePrice'], df_lag['ticker']

    df = pd.concat([df_main, df_lag], axis=1)
    df['tick_pre'] = [np.NAN] + list(df['ticker'].values[:-1])
    df['tick_aft'] = list(df['ticker'].values[1:]) + [np.NAN]
    df['new_main'] = df['tick_pre'] != df['ticker']
    df['new_main_will'] = df['tick_aft'] != df['ticker']

    df['dt'] = df.index
    df['tick_lag'] = df['tick_lag'].fillna('')
    df['diff_lag_main_start'] = (df['closePrice'] - df['lag_pr']) * 1

    df['closePrice_end'], df['lag_pr_end'] = np.transpose(contr_end_val(df['dt closePrice lag_pr ticker tick_lag'.split()]))

    df['diff_lag_main_end'] = (df['closePrice_end'] - df['lag_pr_end']) * 1

    df['tick_aft_kk'] = list(df['ticker'].values[shiftk:]) + [np.NAN] * shiftk

    print (df.loc['2017-08-01':, :])
    df['dt_y'] = df['dt'].apply(lambda xx: xx[:4])
    df['year_new'] = ([np.NAN] + list(df['dt_y'].values[:-1])) != df['dt_y']

    df_ny = df[df['new_main']]
    df_ny.loc[:, 'dtime'] = df['dt'].astype('datetime64[ns]')
    df_ny.loc[:, 'last_contr_pr'] = [np.NAN] + list(df_ny['closePrice'].values[:-1])
    df_ny.loc[:, 'cl_profit'] = df_ny['closePrice_end'] - df_ny['closePrice']
    df_ny.loc[:, 'diff_profit'] = (df_ny['diff_lag_main_end'] - df_ny['diff_lag_main_start'])

    df.loc[:, 'dt'] = df['dt'].astype('str')

    df['diff_lag_main_start_fix'] = np.NAN
    df['diff_lag_main_start_fix'] = df.loc[df['new_main'] | df['new_main_will'], 'diff_lag_main_start']
    df['closePrice_fix'] = np.NAN
    df['closePrice_fix'] = df.loc[df['new_main'] | df['new_main_will'], 'closePrice']

    df['closePrice'] = df['closePrice'].apply(lambda xx: round(xx, 4))
    df['lag_pr'] = df['lag_pr'].apply(lambda xx: round(xx, 4))
    df['diff_lag_main_start'] = df['diff_lag_main_start'].apply(lambda xx: round(xx, 4))

    line1 = Line("", width=1200, height=800)
    line1.add(
        "日线1",
        df['dt'].tolist(),
        df['closePrice'].tolist(),
        yaxis_min=min(df['closePrice'].tolist()),
        yaxis_max=max(df['closePrice'].tolist()),
        yaxis_interval=1,
        tooltip_trigger="axis",
        tooltip_axispointer_type='cross',
        legend_top="3%",
        is_smooth=True,
        line_color='#5296de',
        line_width=2.5,
        is_more_utils=True
        # yaxis_type="log",
    )

    line1.add(
        "日线2",
        df['dt'].tolist(),
        df['lag_pr'].tolist(),
        yaxis_min=min(df['lag_pr'].tolist()),
        yaxis_max=max(df['lag_pr'].tolist()),
        yaxis_interval=1,
        tooltip_trigger="axis",
        tooltip_axispointer_type='cross',
        mark_line=["max", 'average', 'min'],
        legend_top="3%",
        mark_point=['average', 'max', 'min'],
        is_smooth=True,
        is_datazoom_show=True,
        datazoom_xaxis_index=[0, 1],
        line_color='#632418',
        line_width=2.5,
        is_more_utils=True
        # yaxis_type="log",
    )

    line2 = Line("{}{}贴升水收益".format(contract, aft_emptycontr), width=1200, height=400)
    line2.add(
        "日收益",
        df['dt'].tolist(),
        df['diff_lag_main_start'].tolist(),
        yaxis_min=min(df['diff_lag_main_start'].tolist()),
        yaxis_max=max(df['diff_lag_main_start'].tolist()),
        tooltip_trigger="axis",
        tooltip_axispointer_type='cross',
        yaxis_interval=1,
        mark_line=["max", 'average', 'min'],
        legend_top="50%",
        mark_point=['average', 'max', 'min'],
        is_smooth=True,
        is_datazoom_show=True,
        line_color='#082039',
        line_width=3,
        is_more_utils=True
        # yaxis_type="log",
    )

    grid = Grid('贴升水套利', width=1200, height=1600)
    grid.add(line1, grid_bottom="60%")
    grid.add(line2, grid_top="60%")

    line2.render(PIC_FILE_PATH + '{}{}.png'.format(contract, aft_emptycontr))
    grid.render(FILE_DIR + '{}{}.html'.format(contract, aft_emptycontr))


def compare_2contr_byfixperiod(tick1, tick2, period):
    start_yy = 15
    page = Page('期货套利')
    for yy in range(start_yy, 20):
        tick1_p = tick1 + str(yy - 10) + period if tick1.upper() == tick1 else  tick1 + str(yy) + period
        tick2_p = tick2 + str(yy - 10) + period if tick2.upper() == tick2 else  tick2 + str(yy) + period
        line = ''
        if period == '01': line = compare_2contr(tick1_p, tick2_p, '20%d0801' % (yy - 1), '20%d1215' % (yy - 1), comp='div', iplot=yy - start_yy + 1)
        if period == '05': line = compare_2contr(tick1_p, tick2_p, '20%d1101' % (yy - 1), '20%d0415' % (yy), comp='div', iplot=yy - start_yy + 1)
        if period == '09': line = compare_2contr(tick1_p, tick2_p, '20%d0401' % (yy), '20%d0815' % (yy), comp='div', iplot=yy - start_yy + 1)
        page.add(line)

    page.render(FILE_DIR + '{}-{}.html'.format(tick1, tick2))


def compare_2contr(ticker1, ticker2, beginDate, endDate, comp='div', iplot=0):
    print(ticker1, ticker2, beginDate, endDate)

    df1 = read_uqr_HangQing(ticker1, beginDate, endDate)
    df2 = read_uqr_HangQing(ticker2, beginDate, endDate)
    df2['cl2'] = df2['closePrice']
    df2['main2'] = df2['mainCon']
    df2['opInt2'] = df2['openInt']
    del df2['closePrice'], df2['openInt'], df2['tradeDate'], df2['mainCon']
    df = pd.concat([df1, df2], axis=1)

    df['dt'] = df['tradeDate']
    df['dt'] = df['dt'].astype('str')
    df['diff'] = (df['closePrice'] / (df['cl2'])) if comp == 'div' else (df['closePrice'] - df['cl2'])
    if comp == 'vol_div': df['diff'] = np.log2(df['openInt'] / df['opInt2']) / np.log2(3)
    df['diff'] = df['diff'].apply(lambda xx: round(xx, 4))
    print(df[['dt', 'closePrice', 'cl2', 'diff', 'openInt', 'opInt2']].tail(10))

    line = Line("{}-{}".format(ticker1, ticker2), width=1200, height=400)
    line.add(
        "日收益",
        df['dt'].tolist(),
        df['diff'].tolist(),
        yaxis_min=min(df['diff'].tolist()),
        yaxis_max=max(df['diff'].tolist()),
        yaxis_interval=2,
        tooltip_trigger="axis",
        tooltip_axispointer_type='cross',
        mark_line=["max", 'average', 'min'],
        legend_top="3%",
        is_smooth=True,
        line_color='#082039',
        line_width=3,
        is_more_utils=True
    )
    return line


def calc_bfaf20(ct_cmp, ct_ref, ref_src='uqr', cmp_enddate=''):
    ct_mod = "%s / %s" % (ct_cmp, ct_ref)
    title = ct_mod
    if ct_mod == "j / jm": title = "j - jm*1.33"
    beginDate, endDate = '20130101', '20190101'
    fields = 'closePrice ticker openInt turnoverVol mainCon smainCon tradeDate'.split()
    fields_cmp = fields + ['highestPrice', 'lowestPrice']
    df2 = read_uqr_HangQing(ct_cmp, beginDate, endDate)

    df2 = df2.loc[:, fields_cmp]
    if cmp_enddate: df2 = df2.loc[:cmp_enddate]
    if ref_src == "uqr":
        df_ref = read_uqr_HangQing(ct_ref, beginDate, endDate)
        df_ref = df_ref.loc[:, fields]
        df_ref = df_ref[df_ref['ticker'].str.match('^' + ct_ref + '\d+')]
        prefix = '1' if ct_ref == ct_ref.upper() else ''
        df_ref['cdate'] = df_ref['ticker'].apply(lambda xx: prefix + re.sub('[a-zA-Z]', '', xx, 0))
        df_ref = df_ref.drop_duplicates(subset=['tradeDate', 'cdate'])

        if ct_ref in ["rb", "hc"]:
            df_ref['cdate'] = df_ref['cdate'].apply(lambda xx: xx[:-2] + '09' if xx[-2:] == '10'  else xx[:-2] + '09d' if xx[-2:] == '09' else xx)
        df_ref.set_index(['tradeDate', 'cdate'], inplace=True)
        df_ref = df_ref.sort_index()
    if ref_src == "OANDA":
        df_ref = pd.read_csv('../../data/df_%s.csv' % ct_ref, index_col=[0])

        df_f = read_mc_ct2df('HangQing_investing_byD1', '_id', 'tradeDate', condition={'ticker': 'USD_CNY'}, db="Oanda_info")
        df_f.index = df_f['tradeDate']

        # print df_f.tail(10)
        df_ref['cl'] = df_ref['cl'] * df_f['cl']
        df_ref['turnoverVol'] = 10000
        df_ref['closePrice'] = df_ref['cl']
        df_ref['ticker'] = ct_ref
        # print (df_ref.tail(300))
    df_cmp = df2[df2['ticker'].str.match('^' + ct_cmp + '\d+')]
    prefix = '1' if ct_cmp == ct_cmp.upper() else ''
    df_cmp['cdate'] = df_cmp['ticker'].apply(lambda xx: prefix + re.sub('[a-zA-Z]', '', xx, 0))

    if ct_cmp == "FG":
        df_cmp['cdate'] = df_cmp['cdate'].apply(lambda xx: xx[:2] + '10x' if xx[-2:] == '10'  else xx[:2] + '10' if xx[-2:] == '09' else xx)
        df_cmp['cdate'] = df_cmp['cdate'].apply(lambda xx: '1505x' if xx == '1505'  else '1505' if xx == '1506' else xx)
    if ct_cmp == "MA":
        pass
    if ct_cmp in ["rb", "hc"]:
        df_cmp['cdate'] = df_cmp['cdate'].apply(lambda xx: xx[:-2] + '09' if xx[-2:] == '10'  else xx[:-2] + '09d' if xx[-2:] == '09' else xx)

    # if ref_src=="uqr":
    df_cmp = df_cmp.drop_duplicates(subset=['tradeDate', 'cdate'])
    df_cmp.set_index(['tradeDate', 'cdate'], inplace=True)
    df_cmp = df_cmp[df_cmp['mainCon'] == 1]
    if ref_src == "OANDA":
        df_cmp.index = df_cmp.index.get_level_values(0)
        # df_cmp = df_cmp[df_cmp['mainCon'] == 1]
        # df_cmp = df_cmp.drop_duplicates(subset=['tradeDate'])
        # del df_cmp['cdate']
        # df_cmp.set_index(['tradeDate'], inplace=True)
        # df_comp = oanda_cand(ct_cmp)
        # pass

    df_cmp = df_cmp.sort_index()
    df_cmp.columns = ['cmp_cl', 'cmp_tick', 'cmp_opInt', 'cmp_tv', 'cmp_main', 'cmp_smain', 'cmp_hi', 'cmp_lo']
    print(df_ref.tail(3))
    print(df_cmp.tail(3))

    df = pd.concat([df_ref, df_cmp], axis=1)
    df['cmp_tv'] = df['cmp_tv'].fillna(0)
    df = df[df['cmp_tv'] > 3000]
    # print df

    df['diff'] = df['cmp_cl'] / df['closePrice']  # *2.5
    if ct_mod == "cs / c": df['diff'] = df['cmp_cl'] - df['closePrice']
    if ct_mod == "j / jm": df['diff'] = df['cmp_cl'] - 1.33 * df['closePrice']
    if ct_mod == "j / jm": df['diff'] = df['cmp_cl'] - 3 * df['closePrice'] / 1.66
    if ct_mod == "cu / XCU_USD": df['diff'] = df['cmp_cl'] / (2204 * df['closePrice'])
    if ct_mod == "SR / SUGAR_USD": df['diff'] = df['cmp_cl'] / (2204 * df['closePrice'])
    if ct_mod == "a / SOYBN_USD": df['diff'] = df['cmp_cl'] / (36.9 * df['closePrice'])
    if ct_mod == "c / CORN_USD": df['diff'] = df['cmp_cl'] / (39.37 * df['closePrice'])
    if ct_mod == "au / XAU_USD": df['diff'] = df['cmp_cl'] / (df['closePrice'] / 31.3)
    if ct_mod == "ag / XAG_USD": df['diff'] = df['cmp_cl'] / (df['closePrice'] * 1000 / 31.3)

    df['dt'] = df.index.get_level_values(0)
    df['dt'] = df['dt'].astype('str')
    df = df[~df['diff'].isnull()]
    df['diff'] = df['diff'].apply(lambda xx: round(xx, 3))
    if ct_ref == 'c':
        df.loc[(df['dt'] >= '2015-06-23') & (df['dt'] <= '2015-08-17'), 'mainCon'] = 0
        df.loc[(df['dt'] >= '2015-06-23') & (df['dt'] <= '2015-08-17') & (df['ticker'] == 'c1601'), 'mainCon'] = 1
        # df.loc[(df['dt']>='2017-10-01'), 'mainCon'] = 0
        # df.loc[(df['dt']>='2017-10-01') & (df['ticker'] == 'c1805'), 'mainCon'] = 1

    page = Page('期货套利')

    line1 = Line("%s" % ct_cmp, width=1200, height=400)
    line1.add(
        "%s" % ct_cmp,
        df['dt'].tolist(),
        df['cmp_cl'].tolist(),
        yaxis_min=min(df['cmp_cl'].tolist()),
        yaxis_max=max(df['cmp_cl'].tolist()),
        tooltip_trigger="axis",
        tooltip_axispointer_type='cross',
        mark_line=["max", 'average', 'min'],
        mark_point=["max", 'min'],
        mark_point_symbol="circle",
        mark_point_symbolsize=35,
        legend_top="3%",
        is_smooth=True,
        line_color='#632418',
        line_width=2.5,
        is_more_utils=True
        # yaxis_type="log",
    )
    page.add(line1)

    line2 = Line("%s" % ct_ref, width=1200, height=400)
    line2.add(
        "%s" % ct_ref,
        df['dt'].tolist(),
        df['closePrice'].tolist(),
        yaxis_min=min(df['closePrice'].tolist()),
        yaxis_max=max(df['closePrice'].tolist()),
        tooltip_trigger="axis",
        tooltip_axispointer_type='cross',
        mark_line=["max", 'average', 'min'],
        mark_point=["max", 'min'],
        mark_point_symbol="circle",
        mark_point_symbolsize=35,
        legend_top="3%",
        is_smooth=True,
        line_color='#5296de',
        line_width=2.5,
        is_more_utils=True
        # yaxis_type="log",
    )
    page.add(line2)

    line3 = Line("{}-{}套利".format(ct_cmp, ct_ref), width=1200, height=400)
    line3.add(
        "日收益",
        df['dt'].tolist(),
        df['diff'].tolist(),
        yaxis_min=min(df['diff'].tolist()),
        yaxis_max=max(df['diff'].tolist()),
        yaxis_interval=1,
        tooltip_trigger="axis",
        tooltip_axispointer_type='cross',
        mark_line=["max", 'average', 'min'],
        mark_point=["max", 'min'],
        mark_point_symbol="circle",
        mark_point_symbolsize=35,
        legend_top="3%",
        is_smooth=True,
        line_color='#082039',
        line_width=3,
        is_more_utils=True
        # yaxis_type="log",
    )

    page.add(line3)

    line3.render(PIC_FILE_PATH + 'main_{}-{}.png'.format(ct_cmp, ct_ref))
    page.render(FILE_DIR + 'main_{}-{}.html'.format(ct_cmp, ct_ref))

def tiesheng_shui_all():
    tiesheng_shui('p', '1905')
    tiesheng_shui('y', '1905')
    tiesheng_shui('TA', '1905')
    tiesheng_shui('v', '1905')
    tiesheng_shui('pp', '1905')
    tiesheng_shui('l', '1905')
    tiesheng_shui('hc', '1905')
    tiesheng_shui('i', '1905')
    tiesheng_shui('rb', '1905')
    tiesheng_shui('j', '1905')
    tiesheng_shui('jm', '1905')
    tiesheng_shui('zn', '1905')
    tiesheng_shui('pb', '1905')
    tiesheng_shui('al', '1905')
    tiesheng_shui('FG', '1905')


def compare_2contr_byfixperiod_all():
    compare_2contr_byfixperiod('p','y', '05')
    compare_2contr_byfixperiod('OI','y', '05')
    compare_2contr_byfixperiod('OI','RM', '05')
    compare_2contr_byfixperiod('y','m', '05')
    compare_2contr_byfixperiod('RM','m', '05')
    compare_2contr_byfixperiod('cs','c', '05')

    compare_2contr_byfixperiod('v','MA', '05')
    compare_2contr_byfixperiod('pp','MA', '05')
    compare_2contr_byfixperiod('l','MA', '05')
    compare_2contr_byfixperiod('TA','v', '05')
    compare_2contr_byfixperiod('v','l', '05')
    compare_2contr_byfixperiod('l','pp', '05')

    compare_2contr_byfixperiod('hc','rb', '05')
    compare_2contr_byfixperiod('j','jm', '05')
    compare_2contr_byfixperiod('i','rb', '05')
    compare_2contr_byfixperiod('zn','pb', '05')
    compare_2contr_byfixperiod('zn','al', '05')
    compare_2contr_byfixperiod('cu','al', '05')
    compare_2contr_byfixperiod('rb','FG', '05')

def calc_bfaf20_all():
    calc_bfaf20('p', 'y', 'uqr', cmp_enddate='')
    calc_bfaf20('OI', 'y', 'uqr', cmp_enddate='')
    calc_bfaf20('OI', 'RM', 'uqr', cmp_enddate='')
    calc_bfaf20('y', 'm', 'uqr', cmp_enddate='')
    calc_bfaf20('RM', 'm', 'uqr', cmp_enddate='')
    calc_bfaf20('cs', 'c', 'uqr', cmp_enddate='')

    calc_bfaf20('v', 'MA', 'uqr', cmp_enddate='')
    calc_bfaf20('pp', 'MA', 'uqr', cmp_enddate='')
    calc_bfaf20('l', 'MA', 'uqr', cmp_enddate='')
    calc_bfaf20('TA', 'v', 'uqr', cmp_enddate='')
    calc_bfaf20('v', 'l', 'uqr', cmp_enddate='')
    calc_bfaf20('l', 'pp', 'uqr', cmp_enddate='')

    calc_bfaf20('hc', 'rb', 'uqr', cmp_enddate='')
    calc_bfaf20('j', 'jm', 'uqr', cmp_enddate='')
    calc_bfaf20('i', 'rb', 'uqr', cmp_enddate='')
    calc_bfaf20('zn', 'pb', 'uqr', cmp_enddate='')
    calc_bfaf20('zn', 'al', 'uqr', cmp_enddate='')
    calc_bfaf20('cu', 'al', 'uqr', cmp_enddate='')
    calc_bfaf20('rb', 'FG', 'uqr', cmp_enddate='')


if __name__ == '__main__':
    tiesheng_shui_all()
    # calc_bfaf20_all()

