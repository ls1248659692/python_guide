#!/usr/bin/python
# coding=utf8
import pandas as pd
from enum import Enum, unique

__author__ = 'Jam'
__date__ = '2018/12/6 11:34'


@unique
class RunMode(Enum):
    TRADE = "trade"
    BACKTESTING = "backtesting"


class Empty:
    EMPTY_STRING = ""
    EMPTY_INT = 0
    EMPTY_FLOAT = 0.0

class Path:
    STATIC_HTML_PATH = 'mysite/static/html/'
    STATIC_PIC_PATH = 'mysite/static/images/'

class OrderData(object):
    def __init__(self):
        # 　代码编号相关
        self.order_id = Empty.EMPTY_STRING  # 订单编号
        self.instrument = Empty.EMPTY_STRING  # 合约代码
        self.exchange = Empty.EMPTY_STRING  # 交易所代码

        # 　报单相关
        self.price_type = Empty.EMPTY_STRING  # 报单类型
        self.order_price = Empty.EMPTY_FLOAT  # 报单价格
        self.direction = Empty.EMPTY_STRING  # 报单方向，期货用
        self.offset = Empty.EMPTY_STRING  # 报单开平
        self.total_volume = Empty.EMPTY_INT  # 报单总数量
        self.deal_volume = Empty.EMPTY_INT  # 报单成交数量
        self.status = Empty.EMPTY_STRING  # 报单状态

        self.order_time = Empty.EMPTY_STRING  # 发单时间
        self.cancel_time = Empty.EMPTY_STRING  # 撤单时间

        # 　CTP相关
        self.frond_id = Empty.EMPTY_STRING  # 前置机编号，真实交易用
        self.session_id = Empty.EMPTY_STRING  # 连接编号


class DealData(object):
    def __init__(self):
        # 　代码编号相关
        self.trade_id = Empty.EMPTY_STRING  # 成交编号
        self.instrument = Empty.EMPTY_STRING  # 合约代码
        self.exchange = Empty.EMPTY_STRING  # 交易所代码
        self.order_id = Empty.EMPTY_STRING  # 订单编号

        # 　成交相关
        self.deal_price = Empty.EMPTY_FLOAT  # 成交价格
        self.direction = Empty.EMPTY_STRING  # 成交方向，期货用
        self.offset = Empty.EMPTY_STRING  # 成交开平
        self.deal_volume = Empty.EMPTY_INT  # 成交数量
        self.deal_time = Empty.EMPTY_STRING  # 成交时间


class PositionData(object):
    def __init__(self):
        # 　代码编号相关
        self.instrument = Empty.EMPTY_STRING  # 合约代码
        self.exchange = Empty.EMPTY_STRING  # 交易所代码
        self.account_id = Empty.EMPTY_STRING  # 资金账号

        # 　持仓相关
        self.average_price = Empty.EMPTY_FLOAT  # 持仓均价
        self.direction = Empty.EMPTY_STRING  # 持仓方向，期货用
        self.position = Empty.EMPTY_INT  # 持仓数量
        self.frozen = Empty.EMPTY_INT  # 冻结数量
        self.yesterday_position = Empty.EMPTY_INT  # 昨持仓数量，期货用
        self.position_profit = Empty.EMPTY_FLOAT  # 持仓盈亏


class AccountData(object):
    def __init__(self):
        # 账号代码相关
        self.account_id = Empty.EMPTY_STRING  # 资金账号代码

        # 数值相关
        self.pre_balance = Empty.EMPTY_FLOAT  # 昨日账户总资产，期货用
        self.total_balance = Empty.EMPTY_FLOAT  # 账户总资产
        self.available = Empty.EMPTY_FLOAT  # 可用资金


class Environment(object):
    # key 都是每一根bar的timetag
    order_data_dict = {}  # timetag : [order_data,order_data]　　mission_engine risk 之后append
    deal_data_dict = {}  # timetag : [deal_data,deal_data]    broker_engine  deal 之后append
    position_data_dict = {}  # timetag : [position_data,position_data]  broker_engine deal 之后append
    account_data_dict = {}  # timetag : [account_data] ,account_data 只有一个，是当前bar最后一天的,main_engine market_close 之后append

    current_order_data = OrderData()
    current_deal_data = DealData()
    current_position_data = PositionData()
    current_account_data = AccountData()

    bar_order_data_list = []
    bar_deal_data_list = []
    bar_position_data_list = []
    bar_account_data_list = []

    daily_data = pd.DataFrame()
    one_min_data = pd.DataFrame()

    benchmark_index = []

    # 风控部分
    black_namelist = []
    is_pass_risk = True
    is_send_order = False

    # 回测滑点,key是股票，或者具体的期货代码
    slippage_dict = {}
    # 回测手续费,key是股票，或者具体的期货代码
    commission_dict = {}

    # 每根bar结束，清空的当前bar的order 和　deal的list
    @classmethod
    def refresh_list(cls, event):
        cls.bar_order_data_list = []
        cls.bar_deal_data_list = []

    # 回测交易记录
    backtesting_record_order = pd.DataFrame()
    backtesting_record_deal = pd.DataFrame()
    backtesting_record_position = pd.DataFrame()
    backtesting_record_account = pd.DataFrame()

    # 每次下单交易完成，经过回测broker之后清空order和deal的数据，重置是否通过风控
    @classmethod
    def refresh_current_data(cls, event):
        cls.current_order_data = OrderData()
        cls.current_deal_data = DealData()
        cls.current_position_data = PositionData()
        cls.is_pass_risk = True
        cls.is_send_order = False
